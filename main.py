import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import os

# ==============================
# Botの初期設定
# ==============================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# ==============================
# 戦績データの保存先
# ==============================
# Bot稼働中はもちろん、再起動しても戦績が消えないように
# JSONファイル（scores.json）に保存・読み込みを行います。
SCORE_FILE = "scores.json"


def load_scores() -> dict:
    """scores.json からスコアデータを読み込む"""
    if not os.path.exists(SCORE_FILE):
        return {}
    with open(SCORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_scores(scores: dict) -> None:
    """scores.json にスコアデータを書き込む"""
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


def get_user_score(scores: dict, user_id: str) -> dict:
    """指定ユーザーのスコアを取得（無ければ初期値を作成）"""
    if user_id not in scores:
        scores[user_id] = {"win": 0, "lose": 0, "draw": 0}
    return scores[user_id]


# ==============================
# Bot起動時の処理
# ==============================
@bot.event
async def on_ready():
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
    """じゃんけんの勝敗を判定する関数（win / lose / draw を返す）"""
    if user_hand == bot_hand:
        return "draw"

    win_pattern = {
        "グー": "チョキ",
        "チョキ": "パー",
        "パー": "グー",
    }

    if win_pattern[user_hand] == bot_hand:
        return "win"
    else:
        return "lose"


RESULT_TEXT = {
    "win": "あなたの勝ち",
    "lose": "あなたの負け",
    "draw": "あいこ",
}


# ==============================
# /janken コマンドグループ
# ==============================
# 「/janken play」「/janken score」のように、
# 1つの親コマンド(janken)の下に複数の子コマンドをぶら下げる形にします。
janken_group = app_commands.Group(name="janken", description="じゃんけんBotのコマンド")


@janken_group.command(name="play", description="Botとじゃんけんをします")
@app_commands.describe(hand="グー・チョキ・パーから選んでください")
@app_commands.choices(hand=JANKEN_CHOICES)
async def janken_play(interaction: discord.Interaction, hand: app_commands.Choice[str]):
    user_hand = hand.value
    bot_hand = random.choice(["グー", "チョキ", "パー"])

    result = judge(user_hand, bot_hand)

    # ---- 戦績を更新して保存 ----
    scores = load_scores()
    user_id = str(interaction.user.id)
    user_score = get_user_score(scores, user_id)
    user_score[result] += 1
    save_scores(scores)

    embed = discord.Embed(
        title="じゃんけんぽん！",
        description=(
            f"あなた: **{user_hand}**\n"
            f"Bot: **{bot_hand}**\n\n"
            f"結果: **{RESULT_TEXT[result]}**"
        ),
        color=discord.Color.blue(),
    )

    await interaction.response.send_message(embed=embed)


@janken_group.command(name="score", description="自分のじゃんけん戦績を確認します")
async def janken_score(interaction: discord.Interaction):
    scores = load_scores()
    user_id = str(interaction.user.id)
    user_score = get_user_score(scores, user_id)

    win = user_score["win"]
    lose = user_score["lose"]
    draw = user_score["draw"]
    total = win + lose + draw

    if total == 0:
        description = "まだ対戦記録がありません。`/janken play` で対戦してみましょう！"
    else:
        win_rate = win / total * 100
        description = (
            f"対戦数: **{total}**\n"
            f"勝ち: **{win}** / 負け: **{lose}** / あいこ: **{draw}**\n"
            f"勝率: **{win_rate:.1f}%**"
        )

    embed = discord.Embed(
        title=f"{interaction.user.display_name} の戦績",
        description=description,
        color=discord.Color.green(),
    )

    await interaction.response.send_message(embed=embed)


# コマンドグループをBotに登録
bot.tree.add_command(janken_group)


# ==============================
# Botの起動
# ==============================
# ↓↓↓ ここにDiscord Developer Portalで取得したBotトークンを貼り付けてください ↓↓↓
# 例: bot.run("あなたのトークンをここに貼り付ける")
#
# 【注意】
# トークンは絶対に他人に見せたり、GitHubなどに公開したりしないでください。
# トークンが漏れると、あなたのBotを誰でも操作できてしまいます。
import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import os

# ==============================
# Botの初期設定
# ==============================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# ==============================
# 戦績データの保存先
# ==============================
# Bot稼働中はもちろん、再起動しても戦績が消えないように
# JSONファイル（scores.json）に保存・読み込みを行います。
SCORE_FILE = "scores.json"


def load_scores() -> dict:
    """scores.json からスコアデータを読み込む"""
    if not os.path.exists(SCORE_FILE):
        return {}
    with open(SCORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_scores(scores: dict) -> None:
    """scores.json にスコアデータを書き込む"""
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


def get_user_score(scores: dict, user_id: str) -> dict:
    """指定ユーザーのスコアを取得（無ければ初期値を作成）"""
    if user_id not in scores:
        scores[user_id] = {"win": 0, "lose": 0, "draw": 0}
    return scores[user_id]


# ==============================
# Bot起動時の処理
# ==============================
@bot.event
async def on_ready():
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
    """じゃんけんの勝敗を判定する関数（win / lose / draw を返す）"""
    if user_hand == bot_hand:
        return "draw"

    win_pattern = {
        "グー": "チョキ",
        "チョキ": "パー",
        "パー": "グー",
    }

    if win_pattern[user_hand] == bot_hand:
        return "win"
    else:
        return "lose"


RESULT_TEXT = {
    "win": "あなたの勝ち",
    "lose": "あなたの負け",
    "draw": "あいこ",
}


# ==============================
# /janken コマンドグループ
# ==============================
# 「/janken play」「/janken score」のように、
# 1つの親コマンド(janken)の下に複数の子コマンドをぶら下げる形にします。
janken_group = app_commands.Group(name="janken", description="じゃんけんBotのコマンド")


@janken_group.command(name="play", description="Botとじゃんけんをします")
@app_commands.describe(hand="グー・チョキ・パーから選んでください")
@app_commands.choices(hand=JANKEN_CHOICES)
async def janken_play(interaction: discord.Interaction, hand: app_commands.Choice[str]):
    user_hand = hand.value
    bot_hand = random.choice(["グー", "チョキ", "パー"])

    result = judge(user_hand, bot_hand)

    # ---- 戦績を更新して保存 ----
    scores = load_scores()
    user_id = str(interaction.user.id)
    user_score = get_user_score(scores, user_id)
    user_score[result] += 1
    save_scores(scores)

    embed = discord.Embed(
        title="じゃんけんぽん！",
        description=(
            f"あなた: **{user_hand}**\n"
            f"Bot: **{bot_hand}**\n\n"
            f"結果: **{RESULT_TEXT[result]}**"
        ),
        color=discord.Color.blue(),
    )

    await interaction.response.send_message(embed=embed)


@janken_group.command(name="score", description="自分のじゃんけん戦績を確認します")
async def janken_score(interaction: discord.Interaction):
    scores = load_scores()
    user_id = str(interaction.user.id)
    user_score = get_user_score(scores, user_id)

    win = user_score["win"]
    lose = user_score["lose"]
    draw = user_score["draw"]
    total = win + lose + draw

    if total == 0:
        description = "まだ対戦記録がありません。`/janken play` で対戦してみましょう！"
    else:
        win_rate = win / total * 100
        description = (
            f"対戦数: **{total}**\n"
            f"勝ち: **{win}** / 負け: **{lose}** / あいこ: **{draw}**\n"
            f"勝率: **{win_rate:.1f}%**"
        )

    embed = discord.Embed(
        title=f"{interaction.user.display_name} の戦績",
        description=description,
        color=discord.Color.green(),
    )

    await interaction.response.send_message(embed=embed)


# コマンドグループをBotに登録
bot.tree.add_command(janken_group)


# ==============================
# Botの起動
# ==============================
# ↓↓↓ ここにDiscord Developer Portalで取得したBotトークンを貼り付けてください ↓↓↓
# 例: bot.run("あなたのトークンをここに貼り付ける")
#
# 【注意】
# トークンは絶対に他人に見せたり、GitHubなどに公開したりしないでください。
# トークンが漏れると、あなたのBotを誰でも操作できてしまいます。
bot.run(os.environ.get("DISCORD_TOKEN"))
