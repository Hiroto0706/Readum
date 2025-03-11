from fastapi.testclient import TestClient

from src.api.endpoints.quiz import router

client = TestClient(router)


def test_create_quiz():
    """通常の処理"""
    response = client.post(
        "/create_quiz",
        json={
            "type": "text",
            "content": "this is a test content.",
            "difficulty": "intermediate",
            "questionCount": 10,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "preview": {
            "questions": [
                {
                    "content": "この物語の主人公は誰ですか？",
                    "options": {
                        "A": "アリス",
                        "B": "ボブ",
                        "C": "チャーリー",
                        "D": "ダイアン",
                    },
                    "answer": "A",
                    "explanation": "物語の冒頭で主人公として描かれているのはアリスです。",
                },
                {
                    "content": "次のうち、著者の主張に最も近いものはどれですか？",
                    "options": {
                        "A": "技術革新は経済成長の鍵である。",
                        "B": "伝統は未来を切り開く。",
                        "C": "教育は社会を変革する。",
                        "D": "自然との共生が最重要である。",
                    },
                    "answer": "C",
                    "explanation": "本文では、教育の持つ変革力に焦点が当てられています。",
                },
                {
                    "content": "この文章で筆者が最も強調している点は何ですか？",
                    "options": {
                        "A": "革新的なアイデアの重要性",
                        "B": "リスク管理の方法",
                        "C": "持続可能な開発",
                        "D": "グローバル化の影響",
                    },
                    "answer": "C",
                    "explanation": "持続可能な開発が筆者の主張の中心にあるためです。",
                },
            ]
        }
    }
