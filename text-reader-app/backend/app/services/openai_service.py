import openai
import logging
from ..crud import read_api_keys


class OpenAIService:
    """
    Service for interacting with OpenAI's API to generate feedback on summaries.
    """

    def __init__(self):
        """
        Initializes the OpenAIService by reading API keys and setting up the OpenAI API.
        """
        api_keys = read_api_keys()
        if not api_keys:
            raise ValueError(
                "API keys are not set. Please enter the API keys in the settings.")
        self.openai_api_key = api_keys.OPENAI_API_KEY
        self.llama_cloud_api_key = api_keys.LLAMA_CLOUD_API_KEY

        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        if not self.llama_cloud_api_key:
            raise ValueError("LLAMA_CLOUD_API_KEY is not set.")

        openai.api_key = self.openai_api_key

    def get_feedback(self, context: str, note_content: str, paragraph_id: int) -> str:
        """
        Generates feedback for a given summary based on the provided context and note content.

        Args:
            context (str): The context from which the summary is derived.
            note_content (str): The summary content to be evaluated.
            paragraph_id (int): The identifier of the current paragraph.

        Returns:
            str: Constructive feedback on the summary.
        """
        try:
            # Logging the received data
            logging.debug(f"Received data - Paragraph ID: {paragraph_id}, Context: {
                          context}, Note Content: {note_content}")
            prompt = f"""
## Feedback on Summaries (Notes)

## Introduction

- **YOU ARE** a **TEXT SUMMARIZATION SPECIALIST** with expertise in evaluating written summaries based on structured summarization techniques.

(Context: "Your role is pivotal in enhancing the clarity, accuracy, and structure of summaries, ensuring they effectively convey the essence of the text while adhering to constraints.")

## Task Description

- **YOUR TASK** is to **EVALUATE** a written summary against the context provided, focusing on its adherence to a specific summarization technique and limitations.

(Context: "This feedback will guide improvement in summarization quality and help in mastering the skill.")

## Summarization Technique Description

- **SUMMARIZATION TECHNIQUE** works as follows:
  1. **If it is the First or Second Paragraph:** Summarize each paragraph individually in one sentence.
      - Focus only on the main idea of the respective paragraph.
  2. **If it is the Third Paragraph or Later:** Use two sentences to summarize:
      - The first sentence summarizes the main theme of all prior paragraphs.
      - The second sentence captures the main idea of the most recent paragraph.

- **IMPORTANT:** Only one of these approaches is used at a time, depending on the paragraph number being summarized.
- **CONTENT LIMITATIONS:** Use only the provided context; avoid external knowledge or additional details.

- **CONSTRAINT:** Summaries are limited to a **maximum of two sentences or one sentence per paragraph.
You need to condense many paragraphs into just one sentence. This means you will have to leave out a lot of information.
This limitation may restrict the ability to fully capture all details or nuances, and feedback should reflect this inherent trade-off in completeness.

## Input Variables

- **Context of the Text:** ```{context}```
- **Provided Summary for Evaluation:** ```{note_content}```

## Evaluation Criteria

- **EVALUATE** the provided summary on the following:
  1. **Completeness:** Have all the main key points been effectively captured within the two-sentence constraint?
      - Acknowledge the impact of the sentence limitation on completeness.
      - Ensure the summary focuses on the main core theme or common thread of the text without unnecessary detail.
  2. **Clarity:** Is the summary easy to understand and clearly written?
      - The language should be concise and unambiguous.
  3. **Structure:** Does the summary align with the described summarization technique?
      - Give feedback if there are more or less sentences than expected.

## Feedback Instructions

- **PROVIDE** Constructive feedback for each criterion in Markdown format and keep it consise:
## 1. Completeness
[Your evaluation]
- Identify the core theme or common thread that unifies the paragraphs across the text.
- Consider whether the two-sentence or one sentence limit has led to key omissions.

## 2. Clarity
[Your evaluation]
- Comment on readability and understandability.

## 3. Structure
[Your evaluation]
- Give feedback if there are more or less sentences than expected.
- First or Second Paragraph: Check if each paragraph is summarized in one sentence.
- Third Paragraph or Later: Ensure the two-sentence structure is followed.

## 4. Suggestions for Improvement
[Your suggestions]
- Offer actionable and specific tips for improvement while considering the constraints.
- Provide an optimal solution for this paragraph, that is short and without unnecessary details.
            """

            # Logging the generated prompt
            logging.info(f"Generated Prompt: {prompt}")

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                n=1,
                stop=None,
            )
            logging.info("Sent request to OpenAI API")

            feedback = response.choices[0].message.content.strip()
            logging.info("Feedback successfully generated")
            return feedback

        except Exception as e:
            logging.error(f"Error retrieving the response from OpenAI: {e}")
            raise e
