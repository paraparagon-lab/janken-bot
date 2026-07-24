import discord
from discord import app_commands
from discord.ext import commands
import random

# ==============================
# Botの初期設定
# ==============================
# Discord上でBotが必要とする権限（Intents）を設定します。
# じゃんけんBotはメッセージ内容を読む必要がないため、デフォルトのままでOKです。
intents = discord.Intents.default()

# commands.Bot を使うことで、後から機能拡張（Cogなど）もしやすくなります。
# command_prefix は今回スラッシュコマンドのみなので使いませんが、形式上必要です。
bot = commands.Bot(command_prefix="!", intents=intents)


# ==============================
# Bot起動時の処理
# ==============================
@bot.event
async def on_ready():
    # Botが起動したときに一度だけ、スラッシュコマンドをDiscordに登録（同期）します。
    # これを忘れると、コードを書いても /janken コマンドが表示されません。
    try:
        synced = await bot.tree.sync()
        print(f"スラッシュコマンドを {len(synced)} 個同期しました。")
    except Exception as e:
        print(f"コマンド同期でエラーが発生しました: {e}")

    print(f"{bot.user} としてログインしました。")


# ==============================
# じゃんけんの手（グー・チョキ・パー）を選択肢として定義
# ==============================
JANKEN_CHOICES = [
    app_commands.Choice(name="グー", value="グー"),
    app_commands.Choice(name="チョキ", value="チョキ"),
    app_commands.Choice(name="パー", value="パー"),
]


def judge(user_hand: str, bot_hand: str) -> str:
    """じゃんけんの勝敗を判定する関数"""
    if user_hand == bot_hand:
        return "あいこ"

    # 「ユーザーの手: それに勝つ相手の手」の対応表
    win_pattern = {
        "グー": "チョキ",
        "チョキ": "パー",
        "パー": "グー",
    }

    if win_pattern[user_hand] == bot_hand:
        return "あなたの勝ち"
    else:
        return "あなたの負け"


# ==============================
# /janken スラッシュコマンド本体
# ==============================
@bot.tree.command(name="janken", description="Botとじゃんけんをします")
@app_commands.describe(hand="グー・チョキ・パーから選んでください")
@app_commands.choices(hand=JANKEN_CHOICES)
async def janken(interaction: discord.Interaction, hand: app_commands.Choice[str]):
    user_hand = hand.value
    bot_hand = random.choice(["グー", "チョキ", "パー"])

    result = judge(user_hand, bot_hand)

    embed = discord.Embed(
        title="じゃんけんぽん！",
        description=(
            f"あなた: **{user_hand}**\n"
            f"Bot: **{bot_hand}**\n\n"
            f"結果: **{result}**"
        ),
        color=discord.Color.blue(),
    )

    await interaction.response.send_message(embed=embed)


# ==============================
# Botの起動
# ==============================
# ↓↓↓ ここにDiscord Developer Portalで取得したBotトークンを貼り付けてください ↓↓↓
# 例: bot.run("あなたのトークンをここに貼り付ける")
#
# 【注意】
# トークンは絶対に他人に見せたり、GitHubなどに公開したりしないでください。
# トークンが漏れると、あなたのBotを誰でも操作できてしまいます。
import os
bot.run(os.environ.get("DISCORD_TOKEN"))
