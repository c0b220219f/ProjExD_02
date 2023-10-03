import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

bb_imgs = []
for r in range(1, 11):
    bb_img = pg.Surface((20*r, 20*r))
    pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    bb_img.set_colorkey((0, 0, 0))
    bb_imgs.append(bb_img)    
# 演習課題２：拡大爆弾のリストの作成

def check_bd(obj_rct: pg.Rect):
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内にあればTrueなければFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    kk_rev = pg.transform.flip(kk_img,True,False)
    kk_dct = {
        "-5,0": kk_img,
        "-5,-5": pg.transform.rotozoom(kk_img, -45, 1.0),
        "-5,5": pg.transform.rotozoom(kk_img, 45, 1.0),
        "0,-5": pg.transform.rotozoom(kk_rev, 90, 1.0),
        "5,-5": pg.transform.rotozoom(kk_rev, 45, 1.0),
        "5,0": kk_rev,
        "5,5": pg.transform.rotozoom(kk_rev, -45, 1.0),
        "0,5": pg.transform.rotozoom(kk_rev, -90, 1.0),
        "0,0": kk_img
    }  # 演習課題１：切り替え用画像の辞書

    """ばくだん"""
    enn = pg.Surface((20, 20))
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10)
    enn.set_colorkey((0, 0, 0))  # 練習1：爆弾の作成
    
    en_rct = enn.get_rect()  # 練習１：爆弾のrect
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    en_rct.center = (x, y)  # 練習1：爆弾の座標
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(en_rct):
            print("GAME OVER")
            return

        screen.blit(bg_img, [0, 0])
        
        """こうかとん"""
        key_lst = pg.key.get_pressed()
        total_move = [0, 0]
        if key_lst[pg.K_UP]:
            total_move[1] -= 5
        if key_lst[pg.K_DOWN]:
            total_move[1] += 5
        if key_lst[pg.K_LEFT]:
            total_move[0] -= 5
        if key_lst[pg.K_RIGHT]:
            total_move[0] += 5
        kk_rct.move_ip(total_move)
        if check_bd(kk_rct) != (True, True):
            kk_rct.move_ip(-total_move[0], -total_move[1])
        screen.blit(kk_dct[",".join(map(str,total_move))], kk_rct)  # 演習課題１：飛ぶ方向で画像切り替え

        """爆弾"""
        bb_img = bb_imgs[min(tmr//500, 9)]  # 演習２：時間経過で爆弾を大きくする
        en_check = check_bd(en_rct)
        if not en_check[0]:
            vx *= -1
        if not en_check[1]:
            vy *= -1
        en_rct.move_ip(vx, vy)
        screen.blit(bb_img, en_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()