from typing import Any, Optional, Iterable
import my_driver
import weakref


class Node:
    def __init__(self, data: Any, next_node: Optional["Node"] = None):
        self.data = data
        self.next_node = next_node

    def __str__(self):
        return f"({self.data})"

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, value):
        if value is not None and not isinstance(value, Node):
            raise ValueError

        self._next_node = value


class DoubleNode(Node):
    def __init__(
            self, data: Any, next_node: Optional["Node"] = None, prev_node: Optional["Node"] = None
    ):
        super().__init__(data, next_node)
        self.prev_node = prev_node

    def __str__(self):
        return f"[{self.data}]"

    @property
    def prev_node(self):

        return self._prev_node

    @prev_node.setter
    def prev_node(self, value):
        if value is not None and not isinstance(value, Node):
            raise ValueError
        # _prev_node = weakref.ref(value)
        self._prev_node = value


# не используется
class LinkedListIterator:
    def __init__(self, head):
        self.current = head

    def __next__(self):
        if self.current is None:
            raise StopIteration

        node = self.current
        self.current = self.current.next_node
        return node.data

    def __iter__(self):
        return self


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def __str__(self):
        return "->".join(str(node) for node in self._node_iter())

    def __len__(self):
        return self._size

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError

        if item >= len(self) or item < 0:
            raise IndexError

        for i, node in enumerate(self._node_iter()):
            if i == item:
                return node.data

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError

        if key >= len(self) or key < 0:
            raise IndexError

        for i, node in enumerate(self._node_iter()):
            if i == key:
                node.data = value

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        for node in self._node_iter():
            yield node.data

    def _node_iter(self):
        current_node = self.head
        while current_node is not None:
            yield current_node
            current_node = current_node.next_node

    def append(self, data: Any):
        new_node = Node(data)

        for current_node in self._node_iter():
            if current_node.next_node is None:  # tail!
                current_node.next_node = new_node
                break
        else:
            self.head = new_node

        self._size += 1

    def insert(self, data, index=0):
        if index < 0 or index > self._size:
            raise ValueError

        new_node = Node(data)
        self._size += 1
        if index == 0:
            new_node.next_node = self.head
            self.head = new_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    new_node.next_node = node.next_node
                    node.next_node = new_node

    def clear(self):
        self._size = 0
        self.head = None

    def index(self, data: Any):
        for i, node in enumerate(self._node_iter()):
            if node.data == data:
                return i

        raise ValueError

    def delete(self, index: int):
        if index < 0 or index >= self._size:
            raise ValueError

        self._size -= 1
        if index == 0:
            self.head = self.head.next_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    node.next_node = node.next_node.next_node


class LinkedListWithDriver(LinkedList):
    def __init__(self, driver: my_driver.IStructureDriver = None):
        self._driver = driver
        super().__init__()

    @property
    def driver(self) -> my_driver.IStructureDriver:
        if self._driver is None:
            self._driver = my_driver.FabricDriverBuilder.get_driver()
        return self._driver

    def read(self):
        self.clear()
        for item in self.driver.read():
            self.append(item)

    def write(self):
        ll_as_list = [item for item in self]
        self.driver.write(ll_as_list)


def iter_print(seq: Iterable):
    for item in seq:
        print(item)


class Double_LinkedList(LinkedList):

    def __init__(self):

        self.tail = None
        super().__init__()

    def append(self, data: Any):
        new_node = DoubleNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:

            self.tail.prev_node = self.tail
            self.tail = new_node

        self._size += 1



    def insert(self, data, index=0):
        if index < 0 or index > self._size:
            raise ValueError

        new_node = Node(data)
        self._size += 1
        if index == 0:
            new_node.next_node = self.head
            self.head = new_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    new_node.next_node = node.next_node
                    node.next_node = new_node

    def clear(self):
        self._size = 0
        self.head = None

    def index(self, data: Any):
        for i, node in enumerate(self._node_iter()):
            if node.data == data:
                return i

        raise ValueError

    def delete(self, index: int):
        if index < 0 or index >= self._size:
            raise ValueError

        self._size -= 1
        if index == 0:
            self.head = self.head.next_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    node.next_node = node.next_node.next_node


def main():
    # driver = PickleFileDriver("some.bin")
    # ll = LinkedListWithDriver()
    # ll.append("a")
    # ll.append("b")
    # ll.append("c")
    # ll.append("d")
    # ll.append("e")
    # ll.write()
    # print(ll)
    # # ll.driver = JsonFileDriver("some.json")
    # ll.read()
    dll = Double_LinkedList()
    dll.append('a')
    dll.append("b")
    print(dll)
    # iter_print([1, 2, 3, 4])
    # iter_print({1, 2, 3, 4})
    # iter_print("aas")
    # iter_print(ll)

    # {"a": 1}.get("b", 42)


if __name__ == '__main__':
    main()
