
import re
import hashlib
import streamlit as st
from functools import lru_cache


def completion_func(client, message, model_name="llama3.1"):
    completion = client.chat.completions.create(
        model=model_name,
        messages=message,
    )
    return completion


def get_initial_greeting_prompt():
    return "Start the conversation by greeting the candidate and briefly explaining your role."


def get_exit_prompt():
    return (
        "The candidate indicated they want to end the conversation. "
        "Thank them for their time, briefly mention that TalentScout will review their details "
        "and contact them about next steps, and say goodbye in one or two sentences."
    )


def is_exit_intent(user_input):
    exit_keywords = ["exit", "quit", "bye", "goodbye", "that's all", "thats all", "end", "done"]
    return user_input.lower().strip() in exit_keywords



"""
Utility functions for TalentScout AI.
"""


def mask_pii(content: str) -> str:
    """
    Mask personally identifiable information in text.
    Returns content with emails and phone numbers masked.
    """
    content = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[EMAIL]", content)
    content = re.sub(r"\b\d{10,}\b", "[PHONE]", content)
    return content


def build_sanitized_history() -> list:
    """
    Return a version of conversation_history where user PII is masked
    before sending to the model (emails, phone numbers, etc.).
    """
    safe_history = []
    for msg in st.session_state.conversation_history:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            content = mask_pii(content)

        safe_history.append({"role": role, "content": content})
    return safe_history


def init_input_queue():
    """Initialize the input queue in session state if not present."""
    if "input_queue" not in st.session_state:
        st.session_state.input_queue = []
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "response_cache" not in st.session_state:
        st.session_state.response_cache = {}


def add_to_queue(user_input: str) -> bool:
    """
    Add user input to the processing queue.
    Returns True if added successfully, False if duplicate/empty.
    """
    init_input_queue()
    
    # Validate input
    cleaned_input = user_input.strip()
    if not cleaned_input:
        return False
    
    st.session_state.input_queue.append(cleaned_input)
    return True


def get_next_from_queue() -> str | None:
    """Get the next input from the queue, or None if empty."""
    init_input_queue()
    if st.session_state.input_queue:
        return st.session_state.input_queue.pop(0)
    return None


def has_pending_inputs() -> bool:
    """Check if there are pending inputs in the queue."""
    init_input_queue()
    return len(st.session_state.input_queue) > 0


def clear_queue():
    """Clear all pending inputs from the queue."""
    init_input_queue()
    st.session_state.input_queue = []


def get_cache_key(messages: list) -> str:
    """Generate a cache key from the conversation context."""
    context = str(messages[-5:]) if len(messages) > 5 else str(messages)
    return hashlib.md5(context.encode()).hexdigest()


def get_cached_response(messages: list) -> str | None:
    """Check if we have a cached response for this context."""
    init_input_queue()
    cache_key = get_cache_key(messages)
    return st.session_state.response_cache.get(cache_key)


def cache_response(messages: list, response: str):
    """Cache a response for future use. Keeps last 50 responses."""
    init_input_queue()
    cache_key = get_cache_key(messages)
    
    # Limit cache size
    if len(st.session_state.response_cache) >= 50:
        oldest_key = next(iter(st.session_state.response_cache))
        del st.session_state.response_cache[oldest_key]
    
    st.session_state.response_cache[cache_key] = response


def efficient_completion(client, messages: list, model_name: str, use_cache: bool = True):
    """
    Wrapper for completion_func with caching and efficient processing.
    """
    # Check cache first
    if use_cache:
        cached = get_cached_response(messages)
        if cached:
            return cached
    
    # Make the API call
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    
    response = completion.choices[0].message.content
    
    # Cache the response
    if use_cache:
        cache_response(messages, response)
    
    return response


def validate_input(user_input: str) -> tuple[bool, str]:
    """
    Validate user input and return (is_valid, cleaned_input or error_message).
    """
    if not user_input:
        return False, "Please enter a message."
    
    cleaned = user_input.strip()
    
    if len(cleaned) < 1:
        return False, "Please enter a message."
    
    if len(cleaned) > 5000:
        return False, "Message too long. Please keep it under 5000 characters."
    
    return True, cleaned


def is_processing() -> bool:
    """Check if the system is currently processing a request."""
    init_input_queue()
    return st.session_state.get("processing", False)


def set_processing(state: bool):
    """Set the processing state."""
    init_input_queue()
    st.session_state.processing = state


