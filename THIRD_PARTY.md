# Third-party materials and distribution

## AppWorld

The experiment used AppWorld 0.1.3.post1. Upstream: https://github.com/StonyBrookNLP/appworld

AppWorld's public code is Apache-2.0. Its protected task/app/API-specific portions and their derivatives carry an additional requirement that public redistribution be encrypted. The release therefore transports mixed experiment materials, including selected native state witnesses, message fixtures and response references, inside an encrypted bundle. Original aggregate analyses are included in the same container for a single verified download; this packaging does not claim that every numeric score is independently restricted.

The local decoder uses the upstream AES-256-CFB + PBKDF2-HMAC-SHA256 format with a release-specific public packaging password and salt. The three cryptographic functions in `bundle_codec.py` are excerpted from `src/appworld/common/crypto.py` at upstream commit `42b5bcf3cd334fee33f0c37c02070a9f5807add5` (Apache-2.0). The packaging helper revision is distinct from the AppWorld version used during experiments.

The complete Apache-2.0 text is in `LICENSES/Apache-2.0.txt`. Protected materials retain the upstream encrypted-redistribution condition, stated again inside the bundle. Users may decode locally for inspection and verification. Repacking or republishing protected content must retain the condition.

## tau-bench

Upstream: https://github.com/sierra-research/tau-bench

Experiment revision: `59a200c6d575d595120f1cb70fea53cef0632f6b`.
Copyright (c) 2024 Sierra; MIT license, retained in `LICENSES/tau-bench-MIT.txt`.
The complete environment/database is obtained from upstream. Retained source/response examples and experiment records do not confer broader rights.

## Scope of the repository licenses

The root MIT license covers original software contributions. CC BY 4.0 covers original analytical data and documentation. Neither overrides third-party rights. The paper itself and internal working packages are not part of this release. The public bundle password is not a service credential and does not protect private information; credentials must remain excluded even inside the encrypted archive.
