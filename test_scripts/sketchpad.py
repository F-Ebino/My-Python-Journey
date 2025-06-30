import re
line = "Another one bites the dust,queen,greatest hits,55,100,217103, Rock"

columns_list= re.findall(r"(.+),(.+),(.+),(.+),(.+),(.+),(.+)", line)

[(name, artist, album, plays, rating, runtime, genre)] = columns_list
#columns_list = [(name, artist, album, count, rating, length, genre)]
print(name, album, rating)

def add_prices(basket):
	# Initialize the variable that will be used for the calculation
    total = 0
	# Iterate through the dictionary items
    for fruit in basket :
		# Add each price to the total calculation
		# Hint: how do you access the values of
		# dictionary items?
        total += basket[fruit]
	# Limit the return value to 2 decimal places
    return round(total, 2)  

groceries = {"bananas": 1.56, "apples": 2.50, "oranges": 0.99, "bread": 4.59, 
	"coffee": 6.99, "milk": 3.39, "eggs": 2.98, "cheese": 5.44}
print(type(groceries))

print(add_prices(groceries)) # Should print 28.44

print(max.__doc__)

class Apple:
    def __init__(self):
        self.color = "red"
        self.flavor = "sweet"
    def cut_open(self):
        fruit = ""
        nuts =[]
        return "2 halves"

honeycrisp = Apple()
print(type(honeycrisp))
print(honeycrisp.color)
print(honeycrisp.cut_open())



FileServer = {"EndUser1": 2.25, "EndUser2": 4.5, 
"EndUser3":  1 , "EndUser4": 3.75, "EndUser5": 0.6, 
"EndUser6": 8
}
FileServer["EndUser3"].append(2)
print(FileServer)

#import annotations
#class Solution:
 #   def twoSum(self, nums: list[int], target: int) -> list[int]:
 #       for i in range(len(nums)):
#          for j in range(i + 1, len(nums)):
 #               if nums[j] == target - nums[i]:
  #                  return [i, j]
        # Return an empty list if no solution is found
   #     return []
    
class Solution(object):
     def twoSum(self, nums, target):
          nums_a = nums
          nums_b = nums
          xa = -1
          for a in nums:
               xb = -1
               xa += 1
          for b in nums:
                 xb+=1
                 if xa != xb:
                         if a + b == target:
                                return [xa, xb]

solution = Solution()
result = solution.twoSum(nums = [3,2,4], target = 6)
print(result)