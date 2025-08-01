from openai.types.chat import ChatCompletionMessageParam

from browser_user.llm.messages import BaseMessage
from browser_user.llm.openai.serializer import OpenAIMessageSerializer


class OpenRouterMessageSerializer:
	"""
	Serializer for converting between custom message types and OpenRouter message formats.

	OpenRouter uses the OpenAI-compatible API, so we can reuse the OpenAI serializer.
	"""

	@staticmethod
	def serialize_messages(messages: list[BaseMessage]) -> list[ChatCompletionMessageParam]:
		"""
		Serialize a list of browser_user messages to OpenRouter-compatible messages.

		Args:
		    messages: List of browser_user messages

		Returns:
		    List of OpenRouter-compatible messages (identical to OpenAI format)
		"""
		# OpenRouter uses the same message format as OpenAI
		return OpenAIMessageSerializer.serialize_messages(messages)
