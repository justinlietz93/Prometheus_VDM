# Rules for Using OpenAI's Vector Store

**Generated on:** October 30, 2025 at 8:05 AM CDT

---

This document synthesizes all technical rules, syntax requirements, and constraints across various API segments into a single, cohesive master list.

---

## 1. Authentication & Authorization

* **API Key Security**:
  * Treat your API key as a secret.
  * Do not share your API key with others.
  * Do not expose your API key in any client-side code (browsers, apps).
  * Securely load API keys from an environment variable or key management service on the server.
  * Admin API keys must be handled with extreme care due to elevated permissions.
  * Implement best practices like regular key rotation and assigning appropriate permissions for Admin API keys.
* **HTTP Authentication Header**:
  * All API requests must include an `Authorization` header.
  * For non-admin API requests, provide API keys via HTTP Bearer authentication in the `Authorization` header, using the format `Authorization: Bearer <OPENAI_API_KEY>`.
  * For Admin API requests, include an `Authorization` header with `Bearer <OPENAI_ADMIN_KEY>`.
* **API Key Usage**:
  * Admin API keys are generated via the API Platform Organization overview and cannot be used for non-administration endpoints.
  * Only Organization Owners can create and utilize Admin API keys.
  * Project API keys for users are not issued via the API; users must authorize themselves to generate keys.
  * Deleting a project API key will result in an error if the key belonged to a service account.
* **Organization/Project Specific Headers**:
  * Pass the `OpenAI-Organization` header to specify an organization if you belong to multiple organizations or access projects through a legacy user API key.
  * Pass the `OpenAI-Project` header to specify a project if you belong to multiple organizations or access projects through a legacy user API key.
* **Beta API Features**:
  * Beta API features (Assistants, Realtime, Certificates) require the `OpenAI-Beta` header to be set (e.g., `assistants=v2`).

---

## 2. General API Usage & Best Practices

* **Request IDs**: Log request IDs in production deployments for more efficient troubleshooting.
* **SDK Usage**: Consider using the `output_text` property in SDKs instead of directly accessing the first item in the `output` array.
* **Error Handling**:
  * Handle unknown Server Events gracefully, as additional events may be added over time.
  * If a Realtime API Client Event references an ID that cannot be found (e.g., `previous_item_id`, `response` to cancel), an error will be returned.

---

## 3. Common Parameter Constraints

* **`Content-Type` Header**: For JSON requests, the `Content-Type` header must be `application/json`.
* **`metadata` Maps (and `attributes` for Vector Store Files)**:
  * Keys must be strings with a maximum length of 64 characters.
  * Values must be strings with a maximum length of 512 characters (or booleans/numbers for `attributes` in Vector Store Files).
  * For the Responses API, `metadata` maps must contain a maximum of 16 key-value pairs.
* **`limit` Parameter (Pagination for Listing Operations)**:
  * Generally, `limit` must be between 1 and 100 (e.g., Responses input items, Evals, Vector Stores, Runs, Run Steps, Invites, Users, Projects, Project Users, Service Accounts, API Keys, Organization/Project Certificates).
  * For Files API (`List files`), `limit` must be between 1 and 10,000.
  * For Project Rate Limits (`List Project Rate Limits`), `limit` defaults to 100.
  * For Usage APIs (Completions, Embeddings, Moderations, Images, Audio, Vector stores, Code interpreter sessions):
    * If `bucket_width=1d`, default is 7, max is 31.
    * If `bucket_width=1h`, default is 24, max is 168.
    * If `bucket_width=1m`, default is 60, max is 1440.
  * For Costs Usage API, `limit` defaults to 7 and must be between 1 and 180.
* **`order` Parameter (Pagination)**:
  * Defaults to `desc` (descending order).
  * Must be `asc` for ascending order or `desc` for descending order.
* **`temperature` and `top_p`**:
  * Generally, alter one or the other, but not both, as they both control randomness.
  * `temperature` must be between 0 and 2 (Chat Completions, Assistants, Runs, Legacy Completions).
  * `temperature` must be between 0 and 1 (Audio Transcription, Audio Translation).
  * `temperature` for Realtime API `Create Session` must be limited to the range \[0.6, 1.2].
  * `top_p` must be between 0 and 1 (Assistants, Runs).
* **`max_output_tokens` / `max_completion_tokens`**:
  * Sets an upper bound for the number of generated tokens.
  * If exceeded, the run will end with status `incomplete`.
  * For Realtime API `Accept call` and `Create Session`, `max_output_tokens` must be an integer between 1 and 4096, or the string "inf".
  * The deprecated `max_tokens` is not compatible with o-series models; use `max_completion_tokens`.
* **`response_format` (JSON Mode)**:
  * If `type` is `json_object` or `json_schema`, the model is ensured to produce valid JSON or match the schema.
  * When using `json_object`, you must explicitly instruct the model to produce JSON via a system or user message to prevent generating an unending stream of whitespace.
* **`finish_reason="length"`**: Message content may be partially cut off if `finish_reason="length"` is returned, indicating the token limit was exceeded.
* **`safety_identifier`**:
  * Should be a string that uniquely identifies each user.
  * Hash usernames or email addresses for `safety_identifier` to avoid sending identifying information.
* **`top_logprobs`**: Must be an integer between 0 and 20.
* **Path Parameters**: All required path parameters (`message_id`, `thread_id`, `run_id`, `key_id`, `invite_id`, `user_id`, `project_id`, `service_account_id`, `rate_limit_id`, `certificate_id`, `response_id`, `eval_id`, `upload_id`, `vector_store_id`, `session_id`, `container_id`, `call_id`) must be provided for their respective endpoints.
* **Time Parameters**:
  * `start_time` (Usage APIs) must be provided as a Unix timestamp (in seconds).
  * `end_time` (Usage APIs) must be exclusive.

---

## 4. API Endpoints & Structure

* **Standard Endpoints**:
  * `POST /v1/responses` (Create a model response)
  * `POST /v1/responses/{response_id}/cancel` (Cancel a response)
  * `GET /v1/responses/{response_id}/input_items` (List input items for a response)
  * `POST /v1/audio/speech` (Create speech)
  * `POST /v1/audio/transcriptions` (Create transcription)
  * `POST /v1/audio/translations` (Create translation)
  * `POST /v1/images/generations` (Create image)
  * `POST /v1/images/edits` (Create image edit)
  * `POST /v1/images/variations` (Create image variation)
  * `POST /v1/embeddings` (Create embeddings)
  * `POST /v1/evals` (Create eval)
  * `POST /v1/evals/{eval_id}` (Update an eval)
  * `POST /v1/fine_tuning/jobs` (Create fine-tuning job)
  * `POST /v1/batches` (Create batch)
  * `POST /v1/files` (Upload file)
  * `GET /v1/files` (List files)
  * `POST /v1/uploads` (Create upload)
  * `POST /v1/uploads/{upload_id}/parts` (Add upload part)
  * `POST /v1/uploads/{upload_id}/complete` (Complete upload)
  * `POST /v1/uploads/{upload_id}/cancel` (Cancel upload)
  * `DELETE /v1/models/{model}` (Delete a fine-tuned model)
  * `POST /v1/moderations` (Create moderation)
  * `POST /v1/vector_stores` (Create vector store)
  * `POST /v1/vector_stores/{vector_store_id}/search` (Search vector store)
  * `POST /v1/vector_stores/{vector_store_id}/files` (Create vector store file)
  * `POST /v1/vector_stores/{vector_store_id}/files/{file_id}` (Update vector store file attributes)
  * `DELETE /v1/vector_stores/{vector_store_id}/files/{file_id}` (Delete vector store file)
  * `POST /v1/vector_stores/{vector_store_id}/file_batches` (Create vector store file batch)
  * `POST /v1/chatkit/sessions` (Create ChatKit session)
  * `POST /v1/chatkit/sessions/{session_id}/cancel` (Cancel chat session)
  * `POST /v1/containers` (Create container)
  * `POST /v1/containers/{container_id}/files` (Create container file)
  * `POST /v1/chat/completions` (Create chat completion)
  * `POST /v1/chat/completions/{completion_id}` (Update chat completion)
  * `POST /v1/assistants` (Create assistant)
  * `POST /v1/assistants/{assistant_id}` (Modify assistant)
  * `POST /v1/threads/{thread_id}` (Modify thread)
  * `POST /v1/threads/{thread_id}/messages` (Create message)
  * `POST /v1/realtime/calls` (Create call)
  * `POST /v1/realtime/calls/{call_id}/accept` (Accept call)
  * `POST /v1/realtime/calls/{call_id}/reject` (Reject call)
  * `POST /v1/realtime/calls/{call_id}/refer` (Refer call)
  * `POST /v1/realtime/calls/{call_id}/hangup` (Hang up call)
* **Run Management Endpoints**:
  * `POST /v1/threads/{thread_id}/runs` (Create run)
  * `POST /v1/threads/runs` (Create thread and run)
  * `POST /v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs` (Submit Tool Outputs to Run)
  * `POST /v1/threads/{thread_id}/runs/{run_id}/cancel` (Cancel Run)
* **Object Type (`object` field)**: The `object` field in API responses consistently specifies the type (e.g., `thread.message`, `thread.run`, `organization.project`, `realtime.session`). This field should be validated against the expected type for each API response.

---

## 5. Data Formats & Content

* **Text Input Lengths**:
  * `Audio API (Create speech) input`: Maximum length of 4096 characters.
  * `Image API (Create image) prompt`: Maximum 32000 chars for `gpt-image-1`, 1000 for `dall-e-2`, 4000 for `dall-e-3`.
  * `Image API (Create image edit) prompt`: Maximum 32000 chars for `gpt-image-1`, 1000 for `dall-e-2`.
  * `Embeddings API input`: Cannot exceed 8192 tokens for any embedding model.
  * `Embeddings API input (array)`: If an array, it must be 2048 dimensions or less.
  * `Embeddings API input (total)`: Maximum of 300,000 tokens summed across all inputs in a single request.
  * `Embeddings API input`: Cannot be an empty string.
  * `Assistants API instructions`: Maximum length of 256,000 characters.
  * `Assistants API description`: Maximum length of 512 characters.
  * `Assistants API name`: Maximum length of 256 characters.
* **Image Specifics**:
  * `Image API (Create image)`:
    * `n` (number of images) must be between 1 and 10. For `dall-e-3`, only `n=1` is supported.
    * `response_format` URLs are only valid for 60 minutes.
    * `quality` options are model-specific (e.g., `high`/`medium`/`low` for `gpt-image-1`, `hd`/`standard` for `dall-e-3`, `standard` only for `dall-e-2`).
    * `size` options are model-specific (e.g., `auto`/`1024x1024`/`1536x1024`/`1024x1536` for `gpt-image-1`, `256x256`/`512x512`/`1024x1024` for `dall-e-2`, `1024x1024`/`1792x1024`/`1024x1792` for `dall-e-3`).
    * `background` is only supported for `gpt-image-1` and must be `transparent`, `opaque`, or `auto`. If `transparent`, `output_format` must be `png` or `webp`.
    * `moderation` is only supported for `gpt-image-1` and must be `low` or `auto`.
    * `output_compression` is only for `gpt-image-1` with `webp`/`jpeg` and values 0-100.
    * `output_format` is only for `gpt-image-1` and must be `png`, `jpeg`, or `webp`. `gpt-image-1` always returns base64.
    * `partial_images` must be between 0 and 3.
    * `stream` is only supported for `gpt-image-1`.
    * `style` is only for `dall-e-3` and must be `vivid` or `natural`.
  * `Image API (Create image edit)`:
    * `image`: For `gpt-image-1`, `png`/`webp`/`jpg` < 50MB, up to 16 images. For `dall-e-2`, one square `png` < 4MB.
    * `mask`: Must be a valid `PNG` file, < 4MB, and have the same dimensions as the `image`.
    * `input_fidelity` is only for `gpt-image-1` (not `mini`) and must be `high` or `low`.
  * `Image API (Create image variation)`:
    * `image`: Must be a valid `PNG` file, < 4MB, and square.
* **Audio Specifics**:
  * `Audio API (Create speech)`:
    * `input` text is required and max 4096 characters.
    * `model` is required and must be `tts-1`, `tts-1-hd`, or `gpt-4o-mini-tts`.
    * `voice` is required and must be one of `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `onyx`, `nova`, `sage`, `shimmer`, `verse`.
    * `instructions` do not work with `tts-1` or `tts-1-hd` models.
    * `speed` must be a value from 0.25 to 4.0.
    * `stream_format` set to `sse` is not supported for `tts-1` or `tts-1-hd` models.
  * `Audio API (Create transcription)`:
    * `file` is required and must be an audio file object in `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, or `webm` format.
    * `model` is required and must be `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `whisper-1`, or `gpt-4o-transcribe-diarize`.
    * `chunking_strategy` is required when using `gpt-4o-transcribe-diarize` for inputs longer than 30 seconds.
    * `include logprobs` only works with `response_format: json` and models `gpt-4o-transcribe`/`gpt-4o-mini-transcribe`. It is not supported with `gpt-4o-transcribe-diarize`.
    * `known_speaker_names` supports up to 4 speakers.
    * Each sample in `known_speaker_references` must be between 2 and 10 seconds.
    * `prompt` should match the audio language and is not supported when using `gpt-4o-transcribe-diarize`.
    * For `gpt-4o-transcribe`/`gpt-4o-mini-transcribe`, the only supported `response_format` is `json`.
    * For `gpt-4o-transcribe-diarize`, `diarized_json` is required for speaker annotations.
    * `stream` is not supported for `whisper-1` and will be ignored.
    * `response_format` must be `verbose_json` to use `timestamp_granularities`.
    * `timestamp_granularities` option is not available for `gpt-4o-transcribe-diarize`.
    * Supply the input `language` in ISO-639-1 format to improve accuracy and latency.
  * `Audio API (Create translation)`:
    * `file` is required and must be an audio file object in `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, or `webm` format.
    * `model` is required and must be `whisper-1`.
    * `prompt` for translation should be in English.
* **File Uploads (General)**:
  * `file` is required.
  * `purpose` is required and must be one of `assistants`, `batch`, `fine-tune`, `vision`, `user_data`, or `evals`.
  * Individual files can be up to 512 MB.
  * The total size of all files uploaded by one organization can be up to 1 TB.
  * Assistants API supports files up to 2 million tokens and specific file types.
  * Fine-tuning API only supports `.jsonl` files.
  * Batch API only supports `.jsonl` files up to 200 MB in size.
* **Large File Uploads (`/v1/uploads` endpoints)**:
  * `bytes`, `filename`, `mime_type`, and `purpose` are required when creating an upload.
  * `mime_type` must fall within supported MIME types for the specified file purpose.
  * An `Upload` can accept at most 8 GB in total.
  * Each `Part` in an upload can be at most 64 MB.
  * `part_ids` is required and must be an ordered list to complete an upload.
  * The number of bytes uploaded upon completion must match the number of bytes initially specified.
* **Training Data Formats**:
  * `fine-tuning training_file/validation_file`: Must be formatted as a `JSONL` file and uploaded with the `purpose fine-tune`.
  * `fine-tuning chat model messages`: Input messages may contain text or image content only. Audio and file input messages are not currently supported for fine-tuning.
* **Batch Input File**:
  * `input_file_id` is required.
  * Must be formatted as a `JSONL` file and uploaded with the `purpose batch`.
  * Can contain up to 50,000 requests and be up to 200 MB in size.
* **Batch Request Input Object**:
  * `custom_id` must be unique for each request in a batch.
  * `method` must currently be `POST`.
  * `url` must currently be one of `/v1/chat/completions`, `/v1/embeddings`, or `/v1/completions`.
  * `/v1/embeddings` batches are restricted to a maximum of 50,000 embedding inputs across all requests.
* **Container Files**: Must provide either a `file` (raw content in multipart/form-data) or a `file_id` (in JSON request).
* **Realtime API Audio Formats**:
  * `input_audio_format` (Create Session/Transcription Session): Options are `pcm16`, `g711_ulaw`, or `g711_alaw`. Defaults to `pcm16` for transcription.
  * For `pcm16` input audio, it must be 16-bit PCM at a 24kHz sample rate, single channel (mono), and little-endian byte order.
  * `output_audio_format` (Create Session): Options are `pcm16`, `g711_ulaw`, or `g711_alaw`.
  * `input_audio_buffer.append audio`: Must be Base64-encoded audio bytes and in the format specified by `input_audio_format`. Each chunk can be at most 15 MiB.
  * `output_modalities` array cannot request both "text" and "audio" at the same time.
* **Mutual TLS Certificates**: `content` is required and must be in PEM format when uploading a certificate.

---

## 6. Model Behavior & Versioning

* **Model Variability**: Expect changes in model prompting behavior and outputs between snapshots due to their inherent variability.
* **Model Consistency**:
  * Use pinned model versions to ensure consistent prompting behavior and model output.
  * Implement evals for your applications to ensure consistent prompting behavior and model output.
* **Model Context Window**: The `truncation` parameter set to `disabled` will cause the request to fail with a 400 error if the input size exceeds the model's context window.
* **Reasoning Effort**: The `gpt-5-pro` model defaults to and only supports `high` reasoning effort.
* **Model Specific Parameter Interactions**:
  * `instructions` do not work with `tts-1` or `tts-1-hd` models (Audio API).
  * `chunking_strategy` is required when using `gpt-4o-transcribe-diarize` for inputs longer than 30 seconds (Audio API).
  * `include logprobs` only works with `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` (Audio API).
  * `prompt` is not supported when using `gpt-4o-transcribe-diarize` (Audio API).
  * `response_format: json` is the only supported format for `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` (Audio API).
  * `timestamp_granularities` is not available for `gpt-4o-transcribe-diarize` (Audio API).
  * `background`, `moderation`, `output_compression`, `output_format`, `stream` are only supported for `gpt-image-1` (Image API).
  * `style` is only supported for `dall-e-3` (Image API).
  * `input_fidelity` is only supported for `gpt-image-1` (not `gpt-image-1-mini`) (Image API).
  * `response_format` for image edits/variations is only supported for `dall-e-2`.
  * `dimensions` is only supported in `text-embedding-3` and later models (Embeddings API).
  * The `model` used for `label_model` (Graders API) must support structured outputs.
  * `suffix` is only supported for `gpt-3.5-turbo-instruct` (Legacy Completions API).
  * `stop` is not supported with `o3` and `o4-mini` reasoning models (Chat Completions, Legacy Completions).

---

## 7. Lifecycle & State Management

* **Responses API Cancellation**: Only responses created with the `background` parameter set to `true` can be cancelled.
* **Upload Expiration**: An `Upload` expires after an hour after creation.
* **Upload Completion/Cancellation**:
  * No `Parts` may be added after an `Upload` is completed.
  * No `Parts` may be added after an `Upload` is cancelled.
* **Vector Store File Deletion**: Deleting a vector store file removes it from the vector store but does not delete the file itself from the OpenAI platform. Use the delete file endpoint to delete the file.
* **ChatKit Session Cancellation**: Cancelling a session prevents new requests from using the issued client secret.
* **Realtime API Session Configuration**:
  * Once `tracing` is enabled for a session, its configuration cannot be modified.
  * `speed` can only be changed in between model turns.
  * `voice` can only be updated if there have been no other audio outputs yet (WebSocket `session.update` event) or if the model has not responded with audio at least once (`Create Session`).
  * `model` cannot be changed during a session (WebSocket `session.update` event).
* **Realtime API Client Event `input_audio_buffer.commit`**: Will produce an error if the input audio buffer is empty.
* **Realtime API Client Event `conversation.item.truncate`**: Truncating audio will delete the server-side text transcript.
* **Realtime API Client Event `response.create`**: Only one `Response` can write to the default `Conversation` at a time.
* **Realtime API Client Event `response.cancel`**: If there is no response to cancel, the server will respond with an error.
* **Chat Completion Storage**: Only Chat Completions created with the `store` parameter set to `true` will be returned/modified/deleted via respective `Get`, `List`, `Update`, `Delete` endpoints.
* **Assistant/Thread Modification**:
  * Only the `name` and `metadata` properties of an evaluation can be updated.
  * Only the `metadata` field can be modified for a stored chat completion.
  * Only the `metadata` and `tool_resources` can be modified for a thread.
* **Run State**:
  * `usage` will be `null` if a run/run step is not in a terminal state (e.g., `in_progress`, `queued`).
  * Submit Tool Outputs endpoint can only be used when a run has `status: "requires_action"` and `required_action.type` is `submit_tool_outputs`.
  * Only runs with `status: "in_progress"` can be cancelled.
  * If `max_completion_tokens` or `max_prompt_tokens` is exceeded, the run will end with status `incomplete`.
  * `Run status`: Must be one of `queued`, `in_progress`, `requires_action`, `cancelling`, `cancelled`, `failed`, `completed`, `incomplete`, or `expired`.
  * `Run Step status`: Must be one of `in_progress`, `cancelled`, `failed`, `completed`, or `expired`.
  * `Message status`: Must be one of `in_progress`, `incomplete`, or `completed`.
* **Run/Thread Creation**: If `thread` is omitted during `Create Thread and Run`, an empty thread will be created.

---

## 8. Organization & Project Management

* **Admin API Key Creation**: The `name` is required when creating an Admin API Key. The `value` is only shown upon creation.
* **Invites**:
  * `email` and `role` are required when creating an invite.
  * `role` must be `owner` or `reader`.
  * If `projects` is omitted when creating an invite, the user will be invited to the default project.
  * An invite cannot be deleted if it has already been accepted.
* **Projects**:
  * The `name` is required when creating or modifying a project.
  * Projects can be created and archived, but cannot be deleted.
  * The Default project cannot be archived.
  * Archived projects cannot be used or updated.
  * `geography` parameter (Create Project): Your organization must have access to Data residency functionality to use this field.
* **Project Users**:
  * `role` (owner or member) and `user_id` are required when creating or modifying a project user.
  * Users must already be members of the organization to be added to a project.
* **Project Service Accounts**: The `name` is required when creating a project service account.
* **Project Rate Limits**: Rate limits configured for a project may be equal to or lower than the organization's rate limits.
* **Roles**:
  * For messages, `role` must be `user` or `assistant`.
  * For organization-level (Invites, Modify User), `role` must be `owner` or `reader`.
  * For project-level (Create Project User, Modify Project User), `role` must be `owner` or `member`.

---

## 9. Realtime API Specifics

* **WebRTC SDP**: `sdp` (WebRTC Session Description Protocol offer) is required for `Create call`.
* **Call Acceptance**: `type` is required and must be `realtime` for `Accept call`.
* **Call Rejection**: `status_code` defaults to 603 (Decline) for `Reject call`.
* **Call Referral**: `target_uri` is required for `Refer call`.
* **Instructions following**: The `instructions` provided are not guaranteed to be followed by the model.
* **Client Event `session.update`**:
  * Can update any field except `voice` and `model`.
  * To clear the `instructions` field, pass an empty string.
  * To clear the `tools` field, pass an empty array.
  * To clear the `turn_detection` field, pass `null`.
* **Client Event `input_audio_buffer.append`**: The server will not send a confirmation response to this event.
* **Client Event `input_audio_buffer.commit`**: When Server VAD is disabled, the client must manually send `input_audio_buffer.commit` to commit the audio buffer. Committing will not create a response from the model.
* **Client Event `conversation.item.create`**: Cannot populate assistant audio messages.
* **Client Event `conversation.item.truncate`**: `content_index` must be 0. Only assistant message items can be truncated. If `audio_end_ms` is greater than the actual audio duration, the server will respond with an error.
* **Client Event `response.create`**: Set `conversation` to `none` to create a `Response` that does not write to the default `Conversation`.
* **Server Event `done`**: The `data` property must be `[DONE]`.
* **Server Event `error`**: The `data` property must be an error object.
* **Server Event `conversation.item.input_audio_transcription.completed`**: The transcript may diverge from the model's interpretation and should be treated as a rough guide.

---

## 10. Deprecations

* **Fine-tuning API**:
  * The `hyperparameters` parameter is deprecated and should be passed under the `method` parameter.
  * The `functions` parameter is deprecated.
* **Chat Completions API**:
  * `function_call` is deprecated; use `tool_choice` instead.
  * `functions` is deprecated; use `tools` instead.
  * `max_tokens` is deprecated and not compatible with o-series models; use `max_completion_tokens`.
  * `seed` is deprecated.
  * `user` field is being replaced by `safety_identifier` and `prompt_cache_key`; use `prompt_cache_key` instead.

---

## 11. Security & Data Handling

* **Fine-tuning Checkpoint Permissions**: These endpoints require an admin API key.
* **Model Deletion Permissions**: You must have the `Owner` role in your organization to delete a model.
* **Logging Activation**: An Organization Owner must activate logging in the Data Controls Settings. Once activated, logging cannot be deactivated for security reasons.
* **Image Input Storage**: Image inputs over 8MB will be dropped when `store` is true in Chat Completions.

---

## 12. Audit Logs

* **`bucket_width` for Audit Logs**: Defaults to `1d`. Supported values are `1m`, `1h`, `1d`.
* **Audit Log Object `object` field**: The object type is always `thread.run.step`. *(Note: This appears to be a copy-paste error in the source document, and would logically be an audit log specific object type.)*

---

## 13. Assistants API Specifics

* **General**: `assistant_id` is required for run creation/modification.
* **Tools**: There can be a maximum of 128 tools per assistant.
* **Messages**: `content` and `role` (`user` or `assistant`) are required when creating a message.
* **Runs**:
  * If `model` is provided, it will override the model associated with the assistant.
  * `tool_choice required` means the model must call one or more tools before responding to the user.
  * `tool_choice` defaults to `none` if no tools are present; defaults to `auto` if tools are present.

---

## 14. Legacy Completions API

* **Create Completion**:
  * `model` and `prompt` are required.
  * `best_of`: Results cannot be streamed. If used with `n`, `best_of` must be greater than `n`.
  * `logprobs`: Maximum value is 5.
  * `max_tokens`: The sum of prompt tokens and `max_tokens` cannot exceed the model's context length.
  * `stream`: If set to `true`, tokens will be sent as data-only Server-Sent Events, terminated by a `data: [DONE]` message.

## Key Highlights

* Treat your API key as a secret, never expose it in client-side code, and securely load it from environment variables or a key management service. For Admin API keys, implement regular rotation and assign appropriate permissions.
* All API requests must include an `Authorization` header, providing API keys via HTTP Bearer authentication in the format `Authorization: Bearer <YOUR_API_KEY>`.
* To ensure consistent model behavior and output over time, use pinned model versions and implement evals for your applications.
* When using `response_format` with `json_object`, you must explicitly instruct the model to produce JSON via a system or user message to prevent an unending stream of whitespace.
* Replace deprecated parameters such as `function_call` with `tool_choice`, `functions` with `tools`, and `max_tokens` with `max_completion_tokens` for compatibility with newer models.
* The `max_output_tokens` parameter sets an upper bound on generated tokens; exceeding this limit will cause a run to end with an `incomplete` status and potentially result in truncated message content.
* Individual file uploads are limited to 512 MB, with a total organizational limit of 1 TB. Fine-tuning and batch APIs require files to be in `.jsonl` format.
* Projects can be created and archived but cannot be deleted, and the default project cannot be archived, which impacts data governance and lifecycle management.
* An Organization Owner must activate logging in the Data Controls Settings, and once activated, logging cannot be deactivated for security reasons.
* For Embeddings API, the input cannot exceed 8192 tokens for any embedding model, and the total sum of tokens across all inputs in a single request is limited to 300,000.
