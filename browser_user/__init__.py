import os
from typing import TYPE_CHECKING

from browser_user.logging_config import setup_logging

# Only set up logging if not in MCP mode or if explicitly requested
if os.environ.get('BROWSER_USE_SETUP_LOGGING', 'true').lower() != 'false':
	logger = setup_logging()
else:
	import logging

	logger = logging.getLogger('browser_user')

# Monkeypatch BaseSubprocessTransport.__del__ to handle closed event loops gracefully
from asyncio import base_subprocess

_original_del = base_subprocess.BaseSubprocessTransport.__del__


def _patched_del(self):
	"""Patched __del__ that handles closed event loops without throwing noisy red-herring errors like RuntimeError: Event loop is closed"""
	try:
		# Check if the event loop is closed before calling the original
		if hasattr(self, '_loop') and self._loop and self._loop.is_closed():
			# Event loop is closed, skip cleanup that requires the loop
			return
		_original_del(self)
	except RuntimeError as e:
		if 'Event loop is closed' in str(e):
			# Silently ignore this specific error
			pass
		else:
			raise


base_subprocess.BaseSubprocessTransport.__del__ = _patched_del


# Type stubs for lazy imports - fixes linter warnings
if TYPE_CHECKING:
	from browser_user.agent.prompts import SystemPrompt
	from browser_user.agent.service import Agent
	from browser_user.agent.views import ActionModel, ActionResult, AgentHistoryList
	from browser_user.browser import Browser, BrowserConfig, BrowserContext, BrowserContextConfig, BrowserProfile, BrowserSession
	from browser_user.controller.service import Controller
	from browser_user.dom.service import DomService
	from browser_user.llm.anthropic.chat import ChatAnthropic
	from browser_user.llm.azure.chat import ChatAzureOpenAI
	from browser_user.llm.google.chat import ChatGoogle
	from browser_user.llm.groq.chat import ChatGroq
	from browser_user.llm.ollama.chat import ChatOllama
	from browser_user.llm.openai.chat import ChatOpenAI


# Lazy imports mapping - only import when actually accessed
_LAZY_IMPORTS = {
	# Agent service (heavy due to dependencies)
	'Agent': ('browser_user.agent.service', 'Agent'),
	# System prompt (moderate weight due to agent.views imports)
	'SystemPrompt': ('browser_user.agent.prompts', 'SystemPrompt'),
	# Agent views (very heavy - over 1 second!)
	'ActionModel': ('browser_user.agent.views', 'ActionModel'),
	'ActionResult': ('browser_user.agent.views', 'ActionResult'),
	'AgentHistoryList': ('browser_user.agent.views', 'AgentHistoryList'),
	# Browser components (heavy due to playwright/patchright)
	'Browser': ('browser_user.browser', 'Browser'),
	'BrowserConfig': ('browser_user.browser', 'BrowserConfig'),
	'BrowserSession': ('browser_user.browser', 'BrowserSession'),
	'BrowserProfile': ('browser_user.browser', 'BrowserProfile'),
	'BrowserContext': ('browser_user.browser', 'BrowserContext'),
	'BrowserContextConfig': ('browser_user.browser', 'BrowserContextConfig'),
	# Controller (moderate weight)
	'Controller': ('browser_user.controller.service', 'Controller'),
	# DOM service (moderate weight)
	'DomService': ('browser_user.dom.service', 'DomService'),
	# Chat models (very heavy imports)
	'ChatOpenAI': ('browser_user.llm.openai.chat', 'ChatOpenAI'),
	'ChatGoogle': ('browser_user.llm.google.chat', 'ChatGoogle'),
	'ChatAnthropic': ('browser_user.llm.anthropic.chat', 'ChatAnthropic'),
	'ChatGroq': ('browser_user.llm.groq.chat', 'ChatGroq'),
	'ChatAzureOpenAI': ('browser_user.llm.azure.chat', 'ChatAzureOpenAI'),
	'ChatOllama': ('browser_user.llm.ollama.chat', 'ChatOllama'),
}


def __getattr__(name: str):
	"""Lazy import mechanism - only import modules when they're actually accessed."""
	if name in _LAZY_IMPORTS:
		module_path, attr_name = _LAZY_IMPORTS[name]
		try:
			from importlib import import_module

			module = import_module(module_path)
			attr = getattr(module, attr_name)
			# Cache the imported attribute in the module's globals
			globals()[name] = attr
			return attr
		except ImportError as e:
			raise ImportError(f'Failed to import {name} from {module_path}: {e}') from e

	raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
	'Agent',
	'Browser',
	'BrowserConfig',
	'BrowserSession',
	'BrowserProfile',
	'Controller',
	'DomService',
	'SystemPrompt',
	'ActionResult',
	'ActionModel',
	'AgentHistoryList',
	'BrowserContext',
	'BrowserContextConfig',
	# Chat models
	'ChatOpenAI',
	'ChatGoogle',
	'ChatAnthropic',
	'ChatGroq',
	'ChatAzureOpenAI',
	'ChatOllama',
]
