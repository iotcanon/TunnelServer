from flask import Flask, jsonify
import instaloader

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "OK", 200

def fetch_instagram_profile(username):
    """
    Instaloaderを使用してプロフィール情報を取得する内部関数
    """
    L = instaloader.Instaloader()

    try:
        # プロフィール情報を取得
        profile = instaloader.Profile.from_username(L.context, username)
        
        # 取得成功時、必要なデータを辞書型で返す
        return {
            "success": True,
            "data": {
                "username": profile.username,
                "followers": profile.followers,
                "followees": profile.followees,  # フォロー中の数
                "biography": profile.biography   # 自己紹介文
            }
        }, 200
        
    except instaloader.exceptions.ProfileNotExistsException:
        # アカウントが存在しない場合
        return {
            "success": False,
            "error": f"@{username} というアカウントは見つかりませんでした。"
        }, 404
        
    except Exception as e:
        # その他のエラー
        return {
            "success": False,
            "error": f"予期せぬエラーが発生しました: {str(e)}"
        }, 500

@app.route('/insta-profile/<username>', methods=['GET'])
def get_insta_profile(username):
    """
    GET /insta-profile/{ユーザ名} のエンドポイント
    """
    # 内部関数を呼び出してデータとステータスコードを取得
    response_data, status_code = fetch_instagram_profile(username)
    
    # JSONとしてレスポンスを返す
    return jsonify(response_data), status_code

if __name__ == '__main__':
    # サーバーをポート5000番で起動
    app.run(debug=True, host='0.0.0.0', port=5000)