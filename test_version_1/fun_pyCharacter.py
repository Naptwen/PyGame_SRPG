import random

class character(object):
    max_hp = 5
    max_hit = 1
    max_dep = 1
    max_spd = 2
    max_luk = 1
    max_mov = 3
    max_ran = 1
    name = "c1"
    hp = 5
    hit = 1
    atk = 2
    dep = 1
    spd = 2
    luk = 1
    mov = 3
    ran = 1
    img_c = "c1.png"
    img_f = "c1_face.png"
    tag = None

    def __init__(self, name, hp, hit, atk, dep, spd, luk, mov, ran, img_c, img_f, tag):
        self.max_hp = hp
        self.max_hit = hit
        self.max_atk = atk
        self.max_dep = dep
        self.max_spd = spd
        self.max_luk = luk
        self.max_mov = mov
        self.max_ran = ran
        self.name = name
        self.img_c = img_c
        self.img_f = img_f
        self.tag = tag
        self.hp = hp
        self.hit = hit
        self.atk = atk
        self.dep = dep
        self.spd = spd
        self.luk = luk
        self.mov = mov
        self.ran = ran

    def phase_end(self):
        self.mov = self.max_mov
        self.ran = self.max_ran
        self.hit = self.max_hit

    def attack(self, opp):
        max = 7 - (opp.spd - self.spd)
        if max <= 1:
            max = 2
        dice = random.randrange(1,max)
        if dice >= 6:
            opp.hp -= self.atk * 2 - opp.dep    
            print("[ATTACK] : critical")
            return [2, self.atk * 2 - opp.dep]
        elif 6 > dice > 1:
            opp.hp -= self.atk - opp.dep
            print("[ATTACK] : Hit")
            return [1, self.atk - opp.dep]
        else:
            print("[ATTACK] : miss")
            return [0, 0]

    def die_check(self):
        if self.hp <= 0:
            return 1