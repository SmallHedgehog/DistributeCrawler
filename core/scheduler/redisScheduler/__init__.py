# coding: utf-8

"""
获取并管理Redis实例等
"""

import redis

try:
    import cPickle as pickle
except:
    import pickle


def getRedis(**kwargs):
    """Get the instance of redis."""
    pool = redis.ConnectionPool(**kwargs)
    return redis.Redis(connection_pool=pool)

class baseQueue(object):
    """Base functionality common to queues"""
    def __init__(self, key, **kwargs):
        self.redis = getRedis(**kwargs)
        self.key = key
        # Serializer
        self.serializer = pickle

    def getSize(self):
        """Return the length of the queue"""
        return self.redis.llen(self.key)

    def _pack(self, val):
        """Prepares a message to go into Redis"""
        return self.serializer.dumps(val, 1)

    def _unpack(self, val):
        """Unpacks a message stored in Redis"""
        try:
            return self.serializer.loads(val)
        except TypeError:
            return None

    def extend(self, vals):
        """Extends the elements in the queue"""
        with self.redis.pipeline(transaction=False) as pipe:
            for val in vals:
                pipe.lpush(self.key, self._pack(val))
            pipe.execute()

    def _dump(self, fobj):
        """Destructively dump the contents of the queue into fobj"""
        next = self.redis.rpop(self.key)
        while next:
            fobj.write(next)
            next = self.redis.rpop(self.key)

    def dump_to_file(self, fname, truncate=False):
        """Destructively dump the contents of the queue into fname"""
        if truncate:
            with open(fname, 'w+') as f:
                self._dump(f)
        else:
            with open(fname, 'a+') as f:
                self._dump(f)

    def load(self, fobj):
        """Load the contents of the provided fobj into the queue"""
        try:
            while True:
                self.redis.lpush(self.key, self._pack(self.serializer.load(fobj)))
        except:
            return

    def load_from_file(self, fname):
        """Load the contents of the contents of fname into the queue"""
        with file(fname) as f:
            self.load(f)

    def sismember(self, name, val):
        """Judge a set whether contains val"""
        return self.redis.sismember(name, val)

    def sadd(self, name, val):
        """Add the val to set"""
        self.redis.sadd(name, val)

    def clear(self):
        """Removes all the elements in the queue"""
        self.redis.delete(self.key)

class Queue(baseQueue):
    """Implements a FIFO queue"""
    def __init__(self, key, **kwargs):
        super(Queue, self).__init__(key, **kwargs)

    def push(self, element):
        """Push an element"""
        self.redis.lpush(self.key, self._pack(element))

    def pop(self, block=False):
        """Pop an element"""
        if not block:
            popped = self.redis.rpop(self.key)
        else:
            queue, popped = self.redis.brpop(self.key)
        return self._unpack(popped)

class PriorityQueue(baseQueue):
    """A priority queue"""
    def __init__(self, key, **kwargs):
        super(PriorityQueue, self).__init__(key, **kwargs)

    def getSize(self):
        """Return the length of the queue"""
        return self.redis.zcard(self.key)

    def dump(self, fobj):
        """Destructively dump the contents of the queue into fp"""
        next = self.pop()
        while next:
            self.serializer.dump(next[0], fobj)
            next = self.pop()

    def load(self, fobj):
        """Load the contents of the provided fobj into the queue"""
        try:
            while True:
                value, score = self.serializer.load(fobj)
                self.redis.zadd(self.key, value, score)
        except Exception as e:
            return

    def dump_to_file(self, fname, truncate=False):
        """Destructively dump the contents of the queue into fname"""
        if truncate:
            with file(fname, 'w+') as f:
                self.dump(f)
        else:
            with file(fname, 'a+') as f:
                self.dump(f)

    def load_from_file(self, fname):
        """Load the contents of the contents of fname into the queue"""
        with file(fname) as f:
            self.load(f)

    def extend(self, vals):
        """Extends the elements in the queue."""
        with self.redis.pipeline(transaction=False) as pipe:
            for val, score in vals:
                pipe.zadd(self.key, self._pack(val), score)
            return pipe.execute()

    def pop(self, withscores=False):
        """Get the element with the lowest score, and pop it off"""
        with self.redis.pipeline() as pipe:
            o = pipe.zrange(self.key, 0, 0, withscores=True)
            o = pipe.zremrangebyrank(self.key, 0, 0)
            results, count = pipe.execute()
            if results:
                value, score = results[0]
                value = self._unpack(value)
                if withscores:
                    return (value, score)
                return value
            elif withscores:
                return (None, 0.0)
            return None

    def push(self, value, score):
        '''Add an element with a given score'''
        return self.redis.zadd(self.key, self._pack(value), score)


if __name__ == '__main__':
    b = PriorityQueue('hedgehog', host='120.95.132.153', port=6379)

    b.push('http://www.baidu.com', 5)
    print b.pop()
    print b.getSize()
