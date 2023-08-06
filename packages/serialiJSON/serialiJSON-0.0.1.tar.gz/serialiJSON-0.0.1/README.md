# SerialiJSON

`serialiJSON` is a tool that allows you to convert complex objects to JSON only by inheriting the BaseSerializable class.

### Installation

```
python -m install serialiJSON
```

### Usage

Import `BaseSerializable` class

``` python
from serialiJSON import BaseSerializable
``` 
Define your own class inheriting `BaseSerializable`

``` python
class myClass(BaseSerializable):
	...

myObject = myClass()
```

Convert to `JSON`

``` python
myObject.toJson()
```
An optional `indent`  can be passed into `toJson()` 

Property | Description | type | default
---------|-------------|------|--------
indent| set the indent to pretty-printed | Int | None (most compact)

### Compatible Types
Type	| List mode
--------|----------
str		|	[str]
int		|	[int]
bool	|	[bool]
float	|	[float]


### Real Example
``` python
from serialiJSON import BaseSerializable

class Item(BaseSerializable):
	def __init__(self, itemName, isAlive):
		self.itemName = itemName
		self.isAliva = isAlive

class Pet(BaseSerializable):
	def __init__(self, name, age, favItems):
		self.name = name
		self.age = age
		self.favItems = favItems

class Human(BaseSerializable):
	def __init__(self, name, age, pets):
		self.name = name
		self.age = age
		self.pets = pets

items = [
		Item("snow ball", False),
		Item("tree", True)
	]

pets = [
		Pet("Cat", 12, items), 
		Pet("Dog", 4, items)
	]

human = Human("name", 90, pets)

print(human.toJson(indent=4))
```
### pretty-printed
``` json
{
	"name": "name",
	"age": 90,
	"pets": [
		{
			"name": "Cat",
			"age": 12,
			"favItems": [
				{
					"itemName": "snow ball",
					"isAliva": false
				},
				{
					"itemName": "tree",
					"isAliva": true
				}
			]
		},
		{
			"name": "Dog",
			"age": 4,
			"favItems": [
				{
					"itemName": "snow ball",
					"isAliva": false
				},
				{
					"itemName": "tree",
					"isAliva": true
				}
			]
		}
	]
}
```

### non pretty-printed
``` json
{"name": "name", "age": 90, "pets": [{"name": "Cat", "age": 12, "favItems": [{"itemName": "snow ball", "isAliva": false}, {"itemName": "tree", "isAliva": true}]}, {"name": "Dog", "age": 4, "favItems": [{"itemName": "snow ball", "isAliva": false}, {"itemName": "tree", "isAliva": true}]}]}
```