import re
from pathlib import Path
import torch
import torch.nn.functional as F
from loguru import logger
from transformers import GPT2Tokenizer, GPT2LMHeadModel

DTYPE = torch.float32 if not torch.cuda.is_available() else torch.float16

# warnings.filterwarnings("ignore")
MODEL_CLASSES = {
    "gpt2": (GPT2LMHeadModel, GPT2Tokenizer),
}


def getTokens(tokenizer, l):
    tokenizer.encode()


# the tokenizer does not preserve white space at the front of the string.
# so we will append something else to the front of the string and then remove it after tokenization
def hackyEncode(tokenizer, s):
    return tokenizer.encode('====\n ' + s)[2:]


def hackyWhiteSpaceCutter(prompt):
    return re.search(r'\s*$', prompt).group(0)


def memory_merge(prompt, context, tokenizer, maxHistory=2048):
    assert (prompt + context)
    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False, add_prefix_space=True)
    context_tokens = hackyEncode(tokenizer, hackyWhiteSpaceCutter(prompt) + context)
    context_tokens = context_tokens[-(maxHistory - len(prompt_tokens)):]
    # logger.debug('DECODED CONTEXT TOKENS: `%r`', tokenizer.convert_ids_to_tokens(context_tokens))
    prompt_tokens.extend(context_tokens)
    context_tokens = prompt_tokens
    # logger.debug('DECODED OUTPUT IS: `%r`', tokenizer.decode(context_tokens, clean_up_tokenization_spaces=False))
    # this is a hack and it should be up to the sampler to deal with max size
    if len(context_tokens) > maxHistory:
        logger.error("CONTEXT IS TOO LONG ERROR")
        context_tokens = context_tokens[-maxHistory:]
    return context_tokens


def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float("Inf")):
    """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
        Args:
            logits: logits distribution shape (batch size x vocabulary size)
            top_k > 0: keep only top k tokens with highest probability (top-k filtering).
            top_p > 0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        # scatter sorted tensors to original indexing
        indices_to_remove = sorted_indices_to_remove.scatter(
            dim=-1, index=sorted_indices, src=sorted_indices_to_remove
        )
        logits[indices_to_remove] = filter_value
    return logits



def truncate_multiple_sequences(seqs, max_len=100):
    """Truncate multiple sequences, longest first, removing first."""
    while sum(len(s) for s in seqs) > max_len:
        longest = sorted(seqs, key=len, reverse=True)[0]
        longest.pop(0)


class GPT2Generator:
    def __init__(
            self, generate_num=60, temperature=0.4, top_k=40, top_p=0.9,
            model_path: str="./models/model_v5_pytorch_rus_books_games/", repetition_penalty=1,
    ):
        self.generate_num = generate_num
        self.temp = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.samples = 1
        self.repetition_penalty = repetition_penalty
        self.batch_size = 1
        self.dtype = DTYPE
        self.max_history_tokens = 2048 - generate_num
        self.stop_token = "<|endoftext|>"
        self.checkpoint_path = model_path
        self.device = torch.device("cuda" if self.dtype == torch.float16 else "cpu")
        logger.info(
            "Using device={}, checkpoint={}, dtype={}".format(self.device, str(self.checkpoint_path), self.dtype))

        # Load tokenizer and model
        model_class, tokenizer_class = MODEL_CLASSES["gpt2"]
        self.tokenizer = tokenizer_class.from_pretrained(str(self.checkpoint_path))
        self.model = model_class.from_pretrained(str(self.checkpoint_path))
        self.model.to(self.dtype).to(self.device)
        self.model.eval()

    # def sample_sequence(
    #         self, context_tokens=None, top_k=None, top_p=None, repetition_penalty=None, generate_num=None,
    #         temperature=None, stop_tokens=None
    # ):
    #     assert (top_k is not None)
    #     assert (temperature is not None)
    #     assert (top_p)
    #     assert (repetition_penalty)
    #     generate_num = generate_num if (generate_num is not None) else self.generate_num
    #     temperature = temperature if (temperature is not None) else self.temp
    #     top_k = top_k if top_k is not None else self.top_k
    #     top_p = top_p if top_p is not None else self.top_p
    #     repetition_penalty = repetition_penalty if repetition_penalty is not None else self.repetition_penalty
    #     out = sample_sequence(
    #         model=self.model,
    #         context=context_tokens,
    #         length=generate_num,
    #         # context=self.context,
    #         temperature=temperature,
    #         top_k=top_k,
    #         top_p=top_p,
    #         repetition_penalty=repetition_penalty,
    #         device=self.device,
    #         stop_tokens=stop_tokens,
    #         tokenizer=self.tokenizer
    #         # batch_size=self.batch_size,
    #     )
    #     return out

    # def result_replace(self, result, allow_action=False):
    #     # logger.debug("BEFORE RESULT_REPLACE: `%s`", repr(result))
    #
    #     result = cut_trailing_sentence(result, allow_action=allow_action)
    #
    #     if len(result) == 0:
    #         return ""
    #     first_letter_capitalized = result[0].isupper()
    #     result = result.replace('."', '".')
    #     result = result.replace("#", "")
    #     result = result.replace("*", "")
    #     # TODO look at this I think blank lines should be fine or blacklisted at generation time
    #     result = result.replace("\n\n", "\n")
    #     # result = first_to_second_person(result)
    #
    #     if not first_letter_capitalized:
    #         result = result[0].lower() + result[1:]
    #
    #     # this is annoying since we can already see the AIs output
    #     # logger.debug( "AFTER RESULT_REPLACE: `%r`. allow_action=%r", repr(result), allow_action)
    #
    #     return result
    #
    # def generate_raw(
    #         self, context, prompt='', generate_num=None, temperature=None, top_k=None, top_p=None,
    #         repetition_penalty=None, stop_tokens=None
    # ):
    #     assert (top_k is not None)
    #     assert (temperature is not None)
    #     assert (top_p)
    #     assert (repetition_penalty)
    #
    #     context_tokens = memory_merge(prompt, context, self.tokenizer, self.max_history_tokens)
    #
    #     logger.debug(
    #         "Text passing into model `%r`",
    #         self.tokenizer.decode(
    #             context_tokens,
    #             clean_up_tokenization_spaces=True,
    #             # skip_special_tokens=True,
    #         ),
    #     )
    #     generated = 0
    #     text = ""
    #     for _ in range(self.samples // self.batch_size):
    #         out = self.sample_sequence(
    #             context_tokens,
    #             generate_num=generate_num,
    #             temperature=temperature,
    #             top_k=top_k,
    #             top_p=top_p,
    #             repetition_penalty=repetition_penalty,
    #             stop_tokens=stop_tokens,
    #         )
    #         text += out.text
    #         generated += 1
    #         # disabled clean up of spaces, see what effect this has TODO
    #         if self.stop_token:
    #             index = text.find(self.stop_token)
    #             if index == -1:
    #                 index = None
    #             text = text[:index]
    #         if stop_tokens is not None:
    #             for stop_token in stop_tokens:
    #                 index = text.find(self.stop_token)
    #                 if index == -1:
    #                     index = None
    #                 text = text[:index]
    #     return text

    def generate(self, context, prompt='', temperature=None, top_p=None, top_k=None, repetition_penalty=None, depth=0):
        assert (top_k is not None)
        assert (temperature is not None)
        assert (top_p)
        assert (repetition_penalty)
        # logger.debug("BEFORE PROMPT_REPLACE: `%r`", prompt)

        # prompt = [self.prompt_replace(p) for p in prompt]

        # logger.debug("AFTER PROMPT_REPLACE is: `%r`", repr(prompt))
        assert (prompt + context)

        text = self.generate_raw(
            context, prompt, temperature=temperature, top_k=top_k, top_p=top_p, repetition_penalty=repetition_penalty,
            stop_tokens=self.tokenizer.encode([">"])
        )

        logger.debug("Generated result is: `%r`", repr(text))

        result = self.result_replace(text)

        if (depth > 6) and len(result) == 0:
            # Sometimes it keeps generating a story startng with an action (">"), if it's tried a few times and it keeps
            # happening, lets let it keep action text which starts in ">"
            # We could just blacklist that token and force it to generate something else. TODO
            result = self.result_replace(text, allow_action=True)
            logger.info(
                "Model generated empty text after formatting `%r`. Trying to format less with allow_action=True. `%r`",
                text,
                result,
            )

            # same here as above
        if len(result) == 0:
            if depth < 20:
                logger.info("Model generated empty text trying again %r", depth)
                return self.generate(
                    prompt, context, temperature=temperature, top_p=top_p, top_k=top_k,
                    repetition_penalty=repetition_penalty, depth=depth + 1
                )
            else:
                logger.warn(
                    "Model generated empty text %r times. Try another action", depth
                )
        return result
