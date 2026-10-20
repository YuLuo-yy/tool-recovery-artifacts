# Reading the data

`case_slot` identifies the paired simulation object/world within its batch.
`episode_slot_id` identifies a scheduled trajectory. Neither is a human participant identifier.
`operation`, `split`, `role`, `stage`, `arm`, `presentation`, `repetition` and
`condition_id` define allocation and treatment. Repeated conditions do not add independent worlds.

`strict_state_success` / `state_correct` are binary correctness indicators for the native postcondition.
`report` is the agent's terminal report. Correct-complete requires correct state and `complete`;
false-complete means incorrect state and `complete`. These are separate from extra-effect indicators.
Boolean CSV fields may use `True`/`False`; numeric indicators use 0/1.

`reads`, `writes`, `decisions`, `path`, `unspent_budget` and the first-fresh-read/first-write
positions describe executed behavior. An allowed read is not necessarily executed before a write.
`stale_reads` is a count of potentially stale responses, not a duration.
`model_requests` is a request count; token totals are recorded usage, not a cash invoice.
Recorded wrapper latency is not a controlled end-to-end deployment latency.

`protocol_error` can be a behavioral termination following a technically valid response.
Technical missing records are documented separately in retained inclusion/audit exports; missing
responses are not recoded as model failures. Early exclusions are retained in the S10/C2 frozen exports.
Unknown usage must not be interpreted as zero.

Statistics retain original comparison definitions and correction families:
S11 frozen interval/estimate verification, S12 Holm40, S13 Holm5, S14 Holm2, S15 Holm4.
Percentile bootstrap intervals and sign-flip tests are not inversions of one another.
Use full saved records and the corresponding protocol to interpret denominators and strata.

The protected bundle contains original provenance identifiers so record joins remain possible.
Authentication fields in selected witness exports use the historical deterministic redactions.
Raw and sanitized state hashes refer to different representations; compare like with like.
