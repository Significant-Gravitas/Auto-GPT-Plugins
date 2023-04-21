from gradio_tools import (
    StableDiffusionTool,
    ImageCaptioningTool,
    TextToVideoTool,
    StableDiffusionPromptGeneratorTool,
    WhisperAudioTranscriptionTool,
    DocQueryDocumentAnsweringTool,
    ClipInterrogatorTool,
    ImageToMusicTool,
)
from gradio_tools.tools.gradio_tool import Job
from pathlib import Path
import os


WORKSPACE_DIR = (Path(os.getcwd()) / "auto_gpt_workspace").resolve()


class AutoGPTCaptioner(ImageCaptioningTool):
    def __init__(
        self,
        name="ImageCaptioner",
        description="An image captioner. Use this to create a caption for an image. "
        "Input will be a path to an image file. "
        "The output will be a caption of that image.",
        src="gradio-client-demos/comparing-captioning-models",
        hf_token=None
    ) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"img": "<full-path-to-image>"}

    def create_job(self, query: dict) -> Job:
        for v in query.values():
            if Path(v).exists():
                return super().create_job(v)
            elif Path(WORKSPACE_DIR / v).exists():
                return super().create_job(v)
        raise ValueError(f"Cannot create captioning job for query: {query}")


class AutoGPTStableDiffusion(StableDiffusionTool):
    def __init__(
        self,
        name="StableDiffusion",
        description="An image generator. Use this to generate images based on "
        "text input. Input should be a description of what the image should "
        "look like. The output will be a path to an image file.",
        src="gradio-client-demos/stable-diffusion",
        hf_token=None,
    ) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"prompt": "text description of image"}


class AutoGPTWhisperTool(WhisperAudioTranscriptionTool):
    def __init__(
        self,
        name="Whisper",
        description="A tool for transcribing audio. Use this tool to transcribe an audio file. "
        "track from an image. Input will be a path to an audio file. "
        "The output will the text transcript of that file.",
        src="abidlabs/whisper-large-v2",
        hf_token=None,
    ) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"audio": "full path of audio file"}
    
    def create_job(self, query: dict) -> Job:
        for v in query.values():
            if Path(v).exists():
                return super().create_job(v)
            elif Path(WORKSPACE_DIR / v).exists():
                return super().create_job(v)
        raise ValueError(f"Cannot create transcription job for query: {query}")


class AutoGPTTextToVideoTool(TextToVideoTool):
    def __init__(
        self,
        name="TextToVideo",
        description="A tool for creating videos from text."
        "Use this tool to create videos from text prompts. "
        "Input will be a text prompt describing a video scene. "
        "The output will be a path to a video file.",
        src="damo-vilab/modelscope-text-to-video-synthesis",
        hf_token=None,
    ) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"prompt": "text description of video"}


class AutoGPTPromptGeneratorTool(StableDiffusionPromptGeneratorTool):
    def __init__(
        self,
        name="StableDiffusionPromptGenerator",
        description="Use this tool to improve a prompt for stable diffusion and other image generators "
        "This tool will refine your prompt to include key words and phrases that make "
        "stable diffusion perform better. The input is a prompt text string "
        "and the output is a prompt text string",
        src="microsoft/Promptist",
        hf_token=None,
    ) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"prompt": "text description of image"}


class AutoGPTDocumentAnsweringTool(DocQueryDocumentAnsweringTool):

    def __init__(self, name="DocQuery", description="A tool for answering questions about a document from the from the image of the document. Input will be a two strings separated by a comma: the first will be the path or URL to an image of a document. The second will be your question about the document." "The output will the text answer to your question.", src="abidlabs/docquery", hf_token=None) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"args": "Two strings separated by a comma: the first will be the path or URL to an image of a document. The second will be your question about the document."}


class AutoGPTClipInterrogatorTool(ClipInterrogatorTool):
    def __init__(self, name="ClipInterrogator", description="A tool for reverse engineering a prompt from a source image. " "Use this tool to create a prompt for StableDiffusion that matches the " "input image. The imput is a path to an image. The output is a text string.", src="pharma/CLIP-Interrogator", hf_token=None) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"image": "The full path to the image file"}
    
    def create_job(self, query: dict) -> Job:
        for v in query.values():
            if Path(v).exists():
                return super().create_job(v)
            elif Path(WORKSPACE_DIR / v).exists():
                return super().create_job(v)
        raise ValueError(f"Cannot create transcription job for query: {query}")


class AutoGPTImageToMusicTool(ImageToMusicTool):
    def __init__(self, name="ImagetoMusic", description="A tool for creating music from images. Use this tool to create a musical " "track from an image. Input will be a path to an image file. " "The output will be an audio file generated from that image.", src="fffiloni/img-to-music", hf_token=None) -> None:
        super().__init__(name, description, src, hf_token)
        self.args = {"image": "The full path to the image file"}
    
    def create_job(self, query: dict) -> Job:
        for v in query.values():
            if Path(v).exists():
                return super().create_job(v)
            elif Path(WORKSPACE_DIR / v).exists():
                return super().create_job(v)
        raise ValueError(f"Cannot create img-to-music job for query: {query}")