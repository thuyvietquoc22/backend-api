from app.entity.game.stone import Stone


class TestStone:

    @staticmethod
    def test_stone_eq():
        stone1 = Stone(level=1, color="red", amount=100)
        stone2 = Stone(level=1, color="red", amount=200)
        assert stone1 == stone2

    @staticmethod
    def test_check_duplicate_stone():
        stones = [
            Stone(level=1, color="red", amount=100),
            Stone(level=1, color="blue", amount=200),
            Stone(level=1, color="red", amount=300),
            Stone(level=2, color="red", amount=400),
            Stone(level=2, color="red", amount=500),
            Stone(level=2, color="red", amount=600),
            Stone(level=3, color="red", amount=700),
            Stone(level=3, color="red", amount=800),
            Stone(level=3, color="red", amount=900)
        ]

        assert len(set(stones)) == 4

    @staticmethod
    def test_find_stone():
        stones = [Stone(level=1, color="red", amount=100),
                  Stone(level=1, color="blue", amount=200),
                  Stone(level=1, color="red", amount=300),
                  Stone(level=2, color="red", amount=400),
                  Stone(level=2, color="red", amount=500),
                  Stone(level=2, color="red", amount=600),
                  Stone(level=3, color="red", amount=700),
                  Stone(level=3, color="red", amount=800),
                  Stone(level=3, color="red", amount=900)]

        stone = Stone(level=1, color="red", amount=0)

        index = stones.index(stone)
        assert index == 0

    @staticmethod
    def test_insert_to_stone_list():
        stones = [Stone(level=1, color="red", amount=100),
                  Stone(level=1, color="blue", amount=200),
                  Stone(level=1, color="red", amount=300),
                  Stone(level=2, color="red", amount=400),
                  Stone(level=2, color="red", amount=500),
                  Stone(level=2, color="red", amount=600),
                  Stone(level=3, color="red", amount=700),
                  Stone(level=3, color="red", amount=800),
                  Stone(level=3, color="red", amount=900)]

        stone = Stone(level=1, color="red", amount=100)
        stone.insert_to(stones)

        assert stones[0].amount == 200
        assert len(stones) == 9

    @staticmethod
    def test_insert_to_stone_list_not_existed():
        stones = [Stone(level=1, color="red", amount=100),
                  Stone(level=1, color="blue", amount=200),
                  Stone(level=3, color="red", amount=900)]

        stone = Stone(level=3, color="blue", amount=700)
        stone.insert_to(stones)

        assert stones[-1] == stone
        assert len(stones) == 4

    @staticmethod
    def test_compare_stone():
        stone1 = Stone(level=1, color="red", amount=100)
        stone2 = Stone(level=1, color="red", amount=200)
        stone3 = Stone(level=1, color="blue", amount=100)

        assert not stone1 >= stone2
        assert stone1 <= stone2
        assert stone1 < stone2
        assert not stone1 > stone2
        assert stone1 != stone3
        try:
            stone1 >= stone3
            assert False
        except ValueError:
            assert True
