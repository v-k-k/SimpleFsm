import time
import random
import heapq
from enum import Enum, auto


def random_delay():
	return random.random() * 5
	

def random_countdown():
	return random.randrange(5)


def rockets():
	N = 10_000
	return [
		(random_delay(), random_countdown())
		for _ in range(N)
	]
	

class State(Enum):
	WAITING = auto()
	COUNTING = auto()
	LAUNCHING = auto()
	
	
class Op(Enum):
	WAIT = auto()
	STOP = auto()


class Launch:
	def __init__(self, delay, coundown):
		self._delay = delay
		self._coundown = coundown
		self._state = State.WAITING
		
	def step(self):
		if self._state is State.WAITING:
			self._state = State.COUNTING
			return Op.WAIT, self._delay
			
		if self._state is State.COUNTING:
			if self._coundown == 0:
				self._state = State.LAUNCHING
			else:
				print(f"{self._coundown}...")
				self._coundown -= 1
				if self._coundown == 0:
					self._state = State.LAUNCHING
				return Op.WAIT, 1
			
		if self._state is State.LAUNCHING:
			print("ROCKET launched")
			return Op.STOP, None
			
		assert False, self._state


def now():
	return time.time()


def run(rockets):
	start = now()
	work = [(start, i, Launch(d, c)) for i, (d, c) in enumerate(rockets)]
	while work:
		step_at, id, launch = heapq.heappop(work)
		wait = step_at - now()
		if wait > 0:
			time.sleep(wait)
		op, arg = launch.step()
		if op is Op.WAIT:
			step_at = now() + arg
			heapq.heappush(work, (step_at, id, launch))
		else:
			assert op is Op.STOP
			


if __name__ == "__main__":
	run(rockets())