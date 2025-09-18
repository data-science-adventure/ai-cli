import typer
from typing_extensions import Annotated
from transformers import pipeline
from transformers import pipeline
from PIL import Image
import requests
from PIL import Image
import requests
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
import pandas as pd

# Initialize a Typer application with a help message.
inference_app = typer.Typer(help="Commands for inference operations.")



def get_caption_from_image(image_source):
    """
    Generates a caption for an image using a Hugging Face transformer model.

    Args:
        image_source (str): The file path or URL of the image.

    Returns:
        str: The generated caption for the image.
    """
    try:
        # 1. Create an image-to-text pipeline
        # This will download the model (~1.5 GB) on its first run.
        # The model is 'nlpconnect/vit-gpt2-image-captioning'.
        captioner = pipeline("image-to-text", "ydshieh/vit-gpt2-coco-en", use_fast=True)

        # 2. Generate the caption
        # The pipeline handles loading the image from a URL or local path.
        result = captioner(image_source)

        # The result is a list containing a dictionary.
        caption = result[0]["generated_text"]

        return caption

    except Exception as e:
        return f"An error occurred: {e}"


@inference_app.command()
def sentiment(  # Use Annotated to define a command-line option with rich metadata.
    text: Annotated[
        str,
        typer.Option(
            help="The text to analize for sentiment classification",
            prompt=True,  # Prompts the user for input if not provided
        ),
    ],
):
    """
    This command initiates the model training process.
    """
    classifier = pipeline(
        "sentiment-analysis",
        "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    )

    result = classifier(text)
    print(pd.DataFrame(result))


@inference_app.command()
def image_to_text(
    image_url: Annotated[
        str,
        typer.Option(
            help="Convert image to text",
            prompt=True,  # Prompts the user for input if not provided
        ),
    ],
):
    """
    This command initiates the model training process.
    """

    # 1. Load model, feature extractor, and tokenizer
    model_checkpoint = "nlpconnect/vit-gpt2-image-captioning"
    # By using ViTImageProcessor directly you can specify use_fast
    feature_extractor = ViTImageProcessor.from_pretrained(
        model_checkpoint, use_fast=True
    )
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = VisionEncoderDecoderModel.from_pretrained(model_checkpoint)

    # 2. Load and preprocess the image
    #image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    #image_url = "https://pdollar.github.io/files/images/PiotrDollar.jpg"
    #image_url = "https://cocodataset.org/images/panoptic-splash.png"

    image = Image.open(requests.get(image_url, stream=True).raw).convert("RGB")

    # The feature extractor now returns a dictionary with pixel_values AND attention_mask
    inputs = feature_extractor(images=image, return_tensors="pt")
    pixel_values = inputs.pixel_values

    # 3. Generate the caption, passing the inputs directly
    # This ensures the attention_mask is passed along with the pixel values.
    output_ids = model.generate(
        **inputs, max_length=16, num_beams=4  # Pass the entire inputs dictionary
    )

    # 4. Decode the result
    caption = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()

    print(f"Generated Caption: {caption}")


@inference_app.command()
def ner(
    text: Annotated[
        str,
        typer.Option(
            help="The text to analize",
            prompt=True,  # Prompts the user for input if not provided
        ),
    ],
):
    """
    This command initiates the model training process.
    """
    # You can use a URL to an image on the web...
    ner_tagger = pipeline("ner", aggregation_strategy="simple")
    outputs = ner_tagger(text)
    print(pd.DataFrame(outputs))


@inference_app.command()
def summarization(
    text: Annotated[
        str,
        typer.Option(
            help="The text to analize",
            prompt=True,  # Prompts the user for input if not provided
        ),
    ],
):

    summarizer = pipeline("summarization")
    outputs = summarizer(text, max_length=45, clean_up_tokenization_spaces=True)
    print(outputs[0]['summary_text'])
