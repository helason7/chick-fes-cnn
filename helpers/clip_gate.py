from PIL import Image
import io
import torch
import open_clip

from config.config import DEVICE, CLIP_THRESHOLD, FECES_PROMPTS

clip_model = None
clip_preprocess = None
clip_tokenizer = None

def is_clip_loaded():
    return clip_model is not None

def load_clip():
    global clip_model, clip_preprocess, clip_tokenizer

    clip_model, _, clip_preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="openai"
    )
    clip_model.to(DEVICE).eval()
    clip_tokenizer = open_clip.get_tokenizer("ViT-B-32")


def is_chicken_feces(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = clip_preprocess(image).unsqueeze(0).to(DEVICE)

    text = clip_tokenizer(FECES_PROMPTS).to(DEVICE)

    with torch.no_grad():
        img_feat = clip_model.encode_image(image)
        txt_feat = clip_model.encode_text(text)

        img_feat /= img_feat.norm(dim=-1, keepdim=True)
        txt_feat /= txt_feat.norm(dim=-1, keepdim=True)

        similarity = (img_feat @ txt_feat.T).max().item()

    return similarity >= CLIP_THRESHOLD, similarity
