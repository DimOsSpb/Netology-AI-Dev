# Блок 4.3 - Мультимодальность и streaming

---
## [Репозиторий с работой](https://github.com/DimOsSpb/AI-Dev-Diploma/tree/v0.4.3)

## Результаты
```bash
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ python -m pytest tests/chat/ -v
===================================================================== test session starts ======================================================================
platform linux -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- /home/odv/project/MY/Netology-AI-Dev/Diploma/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/odv/project/MY/Netology-AI-Dev/Diploma
configfile: pyproject.toml
plugins: anyio-4.14.0, langsmith-0.9.4, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 9 items

tests/chat/test_chat.py::test_chat_ok PASSED                                                                                                             [ 11%]
tests/chat/test_chat.py::test_chat_custom_request_id_propagated PASSED                                                                                   [ 22%]
tests/chat/test_chat.py::test_chat_validation_empty_messages PASSED                                                                                      [ 33%]
tests/chat/test_chat.py::test_chat_max_tokens_limit PASSED                                                                                               [ 44%]
tests/chat/test_chat.py::test_chat_assistant_first_message_rejected PASSED                                                                               [ 55%]
tests/chat/test_chat.py::test_chat_temperature_out_of_range PASSED                                                                                       [ 66%]
tests/chat/test_chat.py::test_chat_cache_hit PASSED                                                                                                      [ 77%]
tests/chat/test_stream.py::test_chat_stream PASSED                                                                                                       [ 88%]
tests/chat/test_stream.py::test_chat_stream_content_type_headers PASSED                                                                                  [100%]

====================================================================== 9 passed in 0.25s =======================================================================
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$ python -m pytest tests/bot/ -v
===================================================================== test session starts ======================================================================
platform linux -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- /home/odv/project/MY/Netology-AI-Dev/Diploma/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/odv/project/MY/Netology-AI-Dev/Diploma
configfile: pyproject.toml
plugins: anyio-4.14.0, langsmith-0.9.4, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 17 items

tests/bot/test_backend_client.py::test_get_or_create_chat PASSED                                                                                         [  5%]
tests/bot/test_backend_client.py::test_send_message_parses_sse PASSED                                                                                    [ 11%]
tests/bot/test_backend_client.py::test_send_message_yields_message_saved_event PASSED                                                                    [ 17%]
tests/bot/test_backend_client.py::test_send_message_with_media_attaches_file PASSED                                                                      [ 23%]
tests/bot/test_backend_client.py::test_send_message_ignores_unknown_event_types PASSED                                                                   [ 29%]
tests/bot/test_backend_client.py::test_send_message_skips_lines_without_data_prefix PASSED                                                               [ 35%]
tests/bot/test_backend_client.py::test_clear_messages_sends_delete PASSED                                                                                [ 41%]
tests/bot/test_backend_client.py::test_get_or_create_chat_raises_on_http_error PASSED                                                                    [ 47%]
tests/bot/test_fsm.py::test_ask_flow_states_exist PASSED                                                                                                 [ 52%]
tests/bot/test_fsm.py::test_state_transitions PASSED                                                                                                     [ 58%]
tests/bot/test_fsm.py::test_topics_kb_has_buttons PASSED                                                                                                 [ 64%]
tests/bot/test_fsm.py::test_topics_kb_accepts_custom_topics PASSED                                                                                       [ 70%]
tests/bot/test_web.py::test_notify_requires_token PASSED                                                                                                 [ 76%]
tests/bot/test_web.py::test_notify_rejects_wrong_token PASSED                                                                                            [ 82%]
tests/bot/test_web.py::test_notify_success PASSED                                                                                                        [ 88%]
tests/bot/test_web.py::test_health PASSED                                                                                                                [ 94%]
tests/bot/test_web.py::test_notify_validates_body PASSED                                                                                                 [100%]

====================================================================== 17 passed in 5.96s ======================================================================
(diploma) odv@matebook16s:~/project/MY/Netology-AI-Dev/Diploma$
```
