from random import randint
from dataclasses import  dataclass

# オバブの無差別帯でなぜ急に勝てなくなり、長期的に伸び悩むかをコードでモデリングしてみたもの


@dataclass
class GameMemory:
    partner_level: int
    opponent_avg_level: int

MY_PLAYER_LEVEL = 3

def get_other_matched_player_levels():
    # over帯の無差別級なのでばらつきが大きい。自分を中間程度の強さと仮定する

    return [randint(1, 5) for _ in range(3)]


def get_team_total_strength(team_levels: list[int, int]):
    # ゲームの性質上弱い方のプレイヤーの影響度の方が大きい
    # そのため2人の合計戦力は単純な合計値ではなく、[弱、弱、強]の平均値を基礎値として、ランダム要素として±30%の範囲で変動も加える

    base_strength = (min(team_levels) * 2 + max(team_levels)) / 3

    return base_strength * (1 + randint(-30, 30) / 100)



def main():
    memories = [] 
    # 単純化したモデル内で100回試合を行ったとする
    for _ in range(100):
        other_levels = get_other_matched_player_levels()
        partner_level = other_levels[0]
        my_team_levels = [partner_level , MY_PLAYER_LEVEL]
        opponent_team_levels = other_levels[1:]

        # 試合に勝てたか判定
        my_team_stronger_score = get_team_total_strength(my_team_levels) > get_team_total_strength(opponent_team_levels)
        is_my_team_win = my_team_stronger_score > 0

        # 負けた時の方が記憶に残りやすいので2倍の強さの記憶とみなす
        memories.append(GameMemory(partner_level=partner_level, opponent_avg_level=sum(opponent_team_levels) / 2))
        if not is_my_team_win:
            memories.append(GameMemory(partner_level=partner_level, opponent_avg_level=sum(opponent_team_levels) / 2))
    

    # 過去の試合をまとめて振り返ると、自分より弱い相手と組み、自分より強い相手と対戦との試合が印象に残る
    # その差を埋めるようなプレイスタイルを志向することとなる。ある時点まではプレイヤースキルの向上が必要というフィードバックとなるが、それが難しくなると無茶をするしかなくなり、結果的にプレイスタイルが崩れることになる
    # つまり、試合をするとかえって弱くなってしまうという悪循環に陥る可能性がある
    avg_partner_level = sum([m.partner_level for m in memories]) / len(memories)
    avg_opponent_avg_level = sum([m.opponent_avg_level for m in memories]) / len(memories)
    print(avg_partner_level)
    print(avg_opponent_avg_level)



if __name__ == '__main__':
    main()

