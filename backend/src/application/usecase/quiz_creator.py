from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class QuizCreator:
    # TODO: クイズの生成に必要なプロパティは全てここに書く

    def create_quiz():
        """
        基本的にクイズを生成するフローをここで管理することにする。

        1. 入力を受け取り、テキストスプリットを行う
        →URLの時はFireCrawlを使ってスクレイピングを行う

        2. ベクトルDBに埋め込む

        3. RAG Chainを作成する

        4. Chainの実行
        """

        # TODO: 入力からDocument型のリストを生成する。（Text or URL）
        ### TODO: textかurlかを判断し、Documentを生成するためのインスタンスを作成する
        ### TODO: Documentのリストを生成する関数を叩く

        # TODO: インデックス化し、ベクトルDBにぶちこむ
        ### TODO: ベクトルDBのインスタンスを生成する
        ### TODO: ドキュメントをベクトル化する
        ### TODO: UUIDを生成する
        ### TODO: 保存するベクトルDBのパスを決定する
        ### TODO: ベクトルデータをベクトルDBに保存する

        # TODO: RAG Chainの生成を行う
        ### TODO: プロンプトをpullする
        ### TODO: モデルのインスタンスを作成する
        ### TODO: retrieverのインスタンス作成
        ### TODO: RAG Chainの生成

        # TODO: Chainの実装を行う
        pass
