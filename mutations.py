# class for mutations !!
from settings import BIN
import random
class mutations:
    def __init__(self):
        self.select = {1: self.random_mutate, 2: self.swap_mutate, 3: self.insertion_mutate}

    def random_mutate(self, target_size, member, character_creation):
        ipos = random.randint(0, target_size - 1)
        delta = member.character_creation(target_size)
        member.object = member.object[:ipos] + [delta] + member.object[ipos + 1:]

    def swap_mutate(self, target_size, member, character_creation):
        size=len(member.object)
        ipos = random.randint(0, size - 2)
        ipos2 = random.randint(ipos + 1, size - 1)
        member.object = member.object[:ipos] + [member.object[ipos2]] + member.object[ipos + 1:ipos2] + [
            member.object[ipos]] + member.object[ipos2 + 1:]

    def insertion_mutate(self, target_size, member, character_creation):
        size = len(member.object)
        ipos = random.randint(0, size - 2)
        ipos2 = random.randint(ipos + 1, size - 1)
        member.object = member.object[:ipos] + member.object[ipos + 1:ipos2] + [member.object[ipos]] + member.object[
                                                                                                       ipos2:]
