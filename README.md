## Readum Project

[Readum](https://readum-frontend-996289710696.asia-northeast1.run.app/)は、「読む」を意味する英語 Reading と、「試す」「評価する」を意味するラテン語 testum（英単語 test の語源）を掛け合わせた造語です。

読書というインプットから、自分の理解度を試すアウトプット（クイズ）へと自然につなげる——そんな体験を実現するために名付けました。

Readum の開発スケジュールは以下の Notion にて管理しています。

[Task Management](https://monta-database.notion.site/AI-Qiita-167cca650932800481a5efff0880eb56)

## Readum Design

Readum のデザインはクイズが楽しくなるようなデザインを考えて作りました。

### TOP

<img width="1419" alt="image" src="https://github.com/user-attachments/assets/2d81fce5-9ebe-4464-b774-67fadde42f5d" />

### Test

<img width="1173" alt="image" src="https://github.com/user-attachments/assets/94e73ff1-c5c5-4b7c-9b7b-c7ba93084a94" />

### Result

<img width="1174" alt="image" src="https://github.com/user-attachments/assets/88c372f8-177f-4729-97b6-e66c8d47251e" />

## Readum Directory Configuration

Readum のディレクトリ構成は以下のようになっています。

```
.
├── Makefile
├── README.md
├── backend
│   ├── Dockerfile
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── README.md
│   ├── assets
│   │   ├── document.txt
│   │   └── tmp
│   │       └── faiss
│   ├── config
│   │   └── settings.py
│   ├── main.py
│   ├── src
│   │   ├── api
│   │   │   ├── endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── quiz.py
│   │   │   │   └── result.py
│   │   │   ├── exceptions
│   │   │   │   └── quiz_exceptions.py
│   │   │   └── models
│   │   │       └── quiz.py
│   │   ├── application
│   │   │   ├── exceptions
│   │   │   │   ├── get_result_exceptions.py
│   │   │   │   ├── quiz_creation_exceptions.py
│   │   │   │   └── quiz_submit_exceptions.py
│   │   │   ├── interface
│   │   │   │   └── database_file_handler.py
│   │   │   ├── service
│   │   │   │   └── llm_service.py
│   │   │   └── usecase
│   │   │       ├── get_result.py
│   │   │       ├── quiz_creator.py
│   │   │       └── quiz_submitter.py
│   │   ├── domain
│   │   │   ├── entities
│   │   │   │   ├── question.py
│   │   │   │   ├── quiz.py
│   │   │   │   └── results.py
│   │   │   ├── repositories
│   │   │   │   ├── storage_repository.py
│   │   │   │   └── vectordb_repository.py
│   │   │   └── service
│   │   │       ├── doc_creator.py
│   │   │       └── rag_agent.py
│   │   └── infrastructure
│   │       ├── db
│   │       │   └── vectordb.py
│   │       ├── exceptions
│   │       │   ├── file_system_exceptions.py
│   │       │   ├── llm_exceptions.py
│   │       │   └── vectordb_exceptions.py
│   │       ├── file_system
│   │       │   └── database_file_handler.py
│   │       ├── llm
│   │       │   ├── doc_loader.py
│   │       │   ├── doc_translate.py
│   │       │   └── rag_agent.py
│   │       └── storage
│   │           └── gcs_client.py
│   └── tests
│       ├── api
│       │   └── models
│       │       └── test_api_quiz.py
│       ├── application
│       │   └── usecase
│       │       ├── test_quiz_creator.py
│       │       └── test_quiz_submitter.py
│       ├── conftest.py
│       ├── domain
│       │   └── entities
│       │       ├── test_domain_question.py
│       │       ├── test_domain_quiz.py
│       │       └── test_domain_results.py
│       └── infrastructure
│           ├── llm
│           │   └── test_rag_agent.py
│           └── storage
│               └── test_gcs_client.py
├── docker-compose.prd.yml
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── eslint.config.mjs
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── postcss.config.mjs
│   ├── public
│   │   └── icons
│   ├── src
│   │   ├── app
│   │   │   ├── about
│   │   │   │   └── page.tsx
│   │   │   ├── error.tsx
│   │   │   ├── favicon.ico
│   │   │   ├── layout.tsx
│   │   │   ├── not-found.tsx
│   │   │   ├── opengraph-image.png
│   │   │   ├── page.tsx
│   │   │   └── result
│   │   │       └── [uuid]
│   │   │           ├── opengraph-image.tsx
│   │   │           └── page.tsx
│   │   ├── components
│   │   │   ├── footer
│   │   │   │   └── index.tsx
│   │   │   ├── header
│   │   │   │   └── index.tsx
│   │   │   └── share-link
│   │   │       └── index.tsx
│   │   ├── config.ts
│   │   ├── features
│   │   │   ├── about
│   │   │   │   └── index.tsx
│   │   │   ├── quiz-form
│   │   │   │   ├── actions.ts
│   │   │   │   ├── components
│   │   │   │   │   ├── description
│   │   │   │   │   │   └── index.tsx
│   │   │   │   │   ├── error-message
│   │   │   │   │   │   └── index.tsx
│   │   │   │   │   ├── input-form
│   │   │   │   │   │   ├── actions.ts
│   │   │   │   │   │   ├── components
│   │   │   │   │   │   │   ├── difficulty-level
│   │   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   │   └── types.ts
│   │   │   │   │   │   │   ├── question-count
│   │   │   │   │   │   │   │   └── index.tsx
│   │   │   │   │   │   │   ├── submit-button
│   │   │   │   │   │   │   │   └── index.tsx
│   │   │   │   │   │   │   └── textarea
│   │   │   │   │   │   │       └── index.tsx
│   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   └── types.ts
│   │   │   │   │   └── quiz-list
│   │   │   │   │       ├── components
│   │   │   │   │       │   ├── progress-bar
│   │   │   │   │       │   │   └── index.tsx
│   │   │   │   │       │   ├── question-card
│   │   │   │   │       │   │   └── index.tsx
│   │   │   │   │       │   └── submit-button
│   │   │   │   │       │       └── index.tsx
│   │   │   │   │       └── index.tsx
│   │   │   │   ├── index.tsx
│   │   │   │   └── types.ts
│   │   │   └── result
│   │   │       ├── components
│   │   │       │   ├── result-card
│   │   │       │   │   └── index.tsx
│   │   │       │   └── top-message
│   │   │       │       └── index.tsx
│   │   │       ├── index.tsx
│   │   │       ├── types.ts
│   │   │       └── utils.ts
│   │   └── styles
│   │       └── globals.css
│   └── tsconfig.json
└── infra
    └── terraform
        ├── main.tf
        ├── modules
        │   ├── cloudrun
        │   │   ├── main.tf
        │   │   ├── outputs.tf
        │   │   ├── secrets.tf
        │   │   └── variables.tf
        │   ├── networking
        │   │   ├── main.tf
        │   │   ├── outputs.tf
        │   │   └── variables.tf
        │   ├── secret_manager
        │   │   ├── main.tf
        │   │   ├── outputs.tf
        │   │   └── variables.tf
        │   └── storage
        │       ├── main.tf
        │       ├── outputs.tf
        │       └── variables.tf
        ├── outputs.tf
        ├── providers.tf
        ├── terraform.tfstate
        ├── terraform.tfstate.backup
        ├── terraform.tfvars
        └── variables.tf
```

Readum のバックエンドはドメイン駆動設計を意識した構成になっています。

フロントエンドはコロケーションを意識した設計になっています。
コロケーションとは要するにモジュール性を意識するみたいなニュアンスになっており、個々のコンポーネントの独立性を意識した設計となっています。

Readum のインフラは Terraform にて管理されています。
デプロイには Cloud Run を用いています。
