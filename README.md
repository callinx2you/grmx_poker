# grmx_poker
DP solution for optimal policy on Poker event

## セットアップ
イベントに応じた設定を行う. 例は次節「メインの計算」にて.

- ``--pickup``: イベントのボーナス対象キャラクター名を "-" つなぎで **4 人** 入力する. ``common/grmx_parser.py``に記述された形式であればユニット名での指定も可能.

- ``--titles``: イベント限定称号のあるキャラクターの組み合わせを "-" つなぎで入力する.

- ``--dst``: 結果ファイル名. "results/grmx_policy_${DST}.txt"で出力される. デフォルト名は``default``

(オプション)``--no_reset``: リセット機能なしで実行する.


## メインの計算
``python3 main.py --pickup PICKUP --titles *TITLES --dst DST``

例:
``python3 main.py --pickup TOWA-IBUKI-NOA-SAKI --titles TOWA-IBUKI IBUKI-NOA-SAKI --dst Nov2021``


## 結果ファイルの見方

- ``enum pickups``: キャラクター名に対して番号が割り振られている. 興味のあるキャラクターは``0``以上の番号を, その他は``'OTHERS'``としてまとめ, ``-1``を振ってある.
- ``enum titles``: 称号に対して``0``以上の番号が割り振られている.
- ``result``:
    - ``(n, y, x)``: 状態. 3 変数で記述する.
        - ``n``: 現在の手札の枚数. ( 2 - 6 )
        - ``y``: すでに獲得した称号の内容. enum_titlesの値を用いて, 持っていれば 1, まだ持っていなければ 0 としてbit管理を行う. ( 0 以上, 2^(限定称号の数) 未満 )
        - ``x``: 現在の手札の内容. enum_pickupsの値を用いて, 持っていれば 1, なければ 0 としてbit管理を行う. ( 0 以上, 2^(興味あるキャラクターの数) 未満 )
    - ``policy``: 状態(n, y, x) においてとるべき方策. (``DRAW`` or ``RESET``)
    - ``value``: 状態(n, y, x) の価値. (その状態から称号を全て獲得するまでの手数の期待値に``-1``をかけたもの)
