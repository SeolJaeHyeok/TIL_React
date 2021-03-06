# Arrow Function

일반적으로 함수는 아래와 같은 형태를 지니고 있다.

```javascript
function sayHello(name) {
  return "Hello" + name;
}
```

위와 같은 형태의 함수는 return을 해주지 않으면 **undefined**가 발생하게 된다. 

하지만 Arrow Function은 return을 한다는 게 함축이 되어 있으므로 return을 명시하지 않고도 return이 가능하다.

```javascript
const sayHello = name => "Hello" + name; 
const milkboy = sayHello("milkboy"); 

console.log(milkboy); // Hello milkboy
```

위의 Arrow Function에서 {}를 사용하게 되면 undefined가 발생하게 된다.

```javascript
const sayHello = name => {"Hello" + name}; 
const milkboy = sayHello("milkboy"); 

console.log(milkboy); // undefined
```

왜냐하면 중괄호를 한다는 건 중괄호 안의 어딘가에서 return을 한다는 것을 의미하기 때문이다. 반대로 중괄호를 쓰지 않고 Arrow Function을 사용한다면 return을 한다는 것을 함축하고 있기 때문에 **undefined**가 출력되지 않는다.

또한 Function을 사용할 때 parameter가 있음에도 parameter가 들어오지 않았을 때를 대비하여 default 값을 설정해 줄 수도 있다.

```javascript
function sayHello(name="Stranger") {
  return "Hello" + name;
}

const milkboy = sayHello(); 
console.log(milkboy); // Hello Stranger;
```

```javascript
const sayHello = (name="Stranger") => "Hello" + name; 
const milkboy = sayHello(); 

console.log(milkboy); // Hello Stranger
```

Arrow Function은 이벤트를 추가하거나 Function을 Anonymous Function으로 만들 때 유용하게 사용할 수 있다. [Example](https://codesandbox.io/s/happy-sky-h0btf?file=/src/index.js) 

추가로 Arrow Function은 argument가 두 개 이상일 때 꼭 괄호를 해줘야 한다는 규칙이 있다. 

Arrow Function은 일반적인 함수의 형태보다 깔끔하고 직관적인 코드를 작성할 수 있다는 장점이 있다.

# Object Destructuring

Object Destructuring은 배열이나 객체의 속성을 해체하여 그 값을 개별 변수에 담을 수 있게 하는 JavaScript 표현식이다.

```javascript
const Human = {
  name: "JaeHyeok",
  sex: "Man",
  nationality: "Korea",
  married: false
}

const name = Human.name;
const nationality: Human.nationality;

console.log(`${name}was born in ${nationality}`); 
```

일반적으로 객체의 property에 접근하려면 위와 같이 Object.property와 같이 접근해야 한다. 하지만 이 방법은 효율적인 방식이 아니고 변수명이 겹치게 된다는 단점 또한 존재한다.

이와 같은 문제를 해결할 때 사용할 수 있는게 바로 Object Destructuring(객체 분해 할당)이다. 다시 말해,  Object를 Deconstruct하고 해당 Object에 기반해 새로운 Variable을 만드는 것을 말한다. 

```javascript
const Human = {
  name: "JaeHyeok",
  sex: "Man",
  nationality: "Korea",
  married: false
};

const { name, nationality } = Human;

console.log(`${name} was born in ${nationality}`);
```

Const 이후에 나오는 중괄호는 Object 안에 있는 property(여기서는 name, nationality)들을 가져오는 것을 의미한다. 그런 다음 어떤 Object(여기서는 Human)에서 가져오는지 알려줘야 한다.

여기서 중요한 것은 새로운 variable들은 Object에 기반하여 만들어진다는 것이다. 다시 말해, Human이라는 Object로 가서 name의 값을 name이라는 새로운 변수에 할당하는 것을 말한다. 

만약 Object 내의 존재하는 property와 같은 변수명을 사용하고 싶지 않다면 두 가지의 방법이 있다.

1. 중괄호를 사용하지 않는 방법

```javascript
const Human = {
  name: "JaeHyeok",
  sex: "Man",
  nationality: "Korea",
  married: false
};

const difName = Human.sex; 
const { name, nationality } = Human;

console.log(`${name} was born in ${nationality}. And ${name} is a ${sex}.`);
```

2. 중괄호 내에서 설정하는 방법

```javascript
const Human = {
  name: "JaeHyeok",
  sex: "Man",
  nationality: "Korea",
  married: false
};

const { name, nationality, sex:difName } = Human;

console.log(`${name} was born in ${nationality}. And ${name} is a ${sex}.`);
```

두 번째 방법은 Object로 가서 해당하는 property를 vatiable로 가져온 뒤 그 variable 값을 내가 설정한 variable(여기서는 difName)으로 할당한다는 뜻이다.

위와 같이 한 번만 탐색하는 것이 아니라 더욱 깊게 탐색할 수도 있는데 

```javascript
const Human = {
  name: "JaeHyeok",
  sex: "Man",
  nationality: "Korea",
  favFood: {
    breakfast: "Noodle",
    lunch: "Pizza",
    dinner: "Hamburger"
  }
};

const { name, nationality, favFood: {breakfast, lunch, dinner}} = Human;

console.log(name, nationality, breakfast, lunch, dinner); // output: JaeHyeok Korea Noodle Pizza Hamburger
```

Object안에 Object가 있다면 해당 Object의 property name을 variable로 받아와서 다시 한 번 중괄호를 통해 해당 Object 안으로 들어갈 수 있다. 

[Example](https://codesandbox.io/s/happy-sky-h0btf?file=/src/OD.js)

# Spread Operator

Spread Operator는 특정 객체 또는 배열의 값을 다른 객체, 배열로 복제하거나 옮길 때 사용하고 연산자의 모양은 `...` 이렇게 생겼다.

```javascript
const days = ["Mon", "Tue", "Wed"];
const otherDays = ["Thu", "Fri", "Sat"];

const allDays = days + otherDays;

console.log(allDays); // output: Mon,Tue,WedThu,Fri,Sat
```

위와 같이 배열끼리 더하게 되면 새로운 배열이 만들어지는 것이 아니라 배열 안의 요소를 가진 문자열(string)으로 나타나게 된다. 이렇게 되면 더이상 배열이 아니기 때문에 `array[0]`과 같이 배열 안의 요소에 접근을 할 수 없게 된다.

Spread Operator는 배열들을 Unpack할 때 유용하게 사용할 수 있다. 예를 들어, days 배열과 otherDays 배열이 필요로 한게 아니라 배열 안의 요소들만 필요로 하다면 Spread Operator는 아주 좋은 선택지가 될 것이다. 왜냐하면 내가 원하는 것은 배열을 없애고 배열 안에 들어 있는 요소들만 사용하기를 원하기 때문이다.

Spread Operator는 배열 안의 요소들을 가져와서 Unpack해 준다. 그렇기 때문에 배열 안의 요소들을 전달할 뿐 배열을 전달하지 않는다.

```jsx
const days = ["Mon", "Tue", "Wed"];
const otherDays = ["Thu", "Fri", "Sat"];

const allDays = [...days, ...otherDays];

console.log(allDays); // output: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
```

위와 같이 Spread Operator를 사용하게 되면 두 배열이 가진 요소들을 하나의 배열이 가지게 된다. 또한 Spread Operator는 객체에서도 동작한다.

```javascript
const ob = {
  first: "hi",
  second: "hello"
};

const ab = {
  third: "bye bye"
};

const two = { ...ob, ...ab };

console.log(two); // output: {first: "hi", second: "hello", third: "bye bye"}
```

이렇게 Object에서도 배열에서와 마찬가지로 객체 내의 요소들만 Unpack하여 사용할 수 있게 해 준다.

Spread Operator는 Function와 Argument에서도 동작한다. 

```javascript
const fn = (something, args) => console.log(...args);
```

위와 같이 사용하게 되면 누군가가 제공한 모든 argument에 대하여 `console.log` 를 할 수 있게 된다.

정리하면 Spread Operator는 두 개의 객체나 배열을 병합하거나, 복사본을 만들거나, 어떤 대상의 콘텐츠를 다른 대상으로 넣을 때 유용하게 쓸 수 있는 문법이다.

[Example](https://codesandbox.io/s/happy-sky-h0btf?file=/src/SO.js:153-288)

# Array Method - [MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array)

공부하면서 계속 추가할 예정

## 1. Array.map

`map()` 메서드는 배열 내의 모든 요소 각각에 대하여 주어진 함수를 호출한 결과를 모아 새로운 배열을 반환한다. 다시 말해 `map()` 메서드는 배열의 모든 요소들에 대해 function을 실행하고 그 함수의 결과 값으로 새로운 배열을 만드는 메서드를 뜻한다.

```javascript
const array1 = [1, 4, 9, 16];

// pass a function to map
const map1 = array1.map(x => x * 2);

console.log(map1);
// expected output: Array [2, 8, 18, 32]
```

 [MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/map)

>✅
>
>1. Map 메서드의 경우는 주로 API를 통해 배열을 받아오면 해당 배열의 요소들로 여러 Component들을 만드는 경우가 있는데 이런 경우에 많이 사용했다.

## 2. Array.filter

`filter()` 메서드는 주어진 함수의 테스트를 통과하는 모든 요소를 모아 새로운 배열로 반환한다. 다시 말해, `filter()` 메서드는 배열의 모든 요소들에 대하여 조건식을 통과한 요소들로 이루어진 새로운 배열을 만드는 메서드를 뜻한다. 

```javascript
const words = ['spray', 'limit', 'elite', 'exuberant', 'destruction', 'present'];

const result = words.filter(word => word.length > 6);

console.log(result);
// expected output: Array ["exuberant", "destruction", "present"]
```

[MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)

> ✅
>
> 1. 여러 리액트 프로젝트를 진행하며 느꼈던 점은 filter는 주로 조건을 주고 해당하지 않는 경우를 삭제할 때 요컨대, id나 다른 고유한 값을 주고 그에 해당하는 값와 일치하지 않으면 제거하는 등의 로직(logout, 정보 삭제 등)에서 많이 사용했었다.

## 3. Array.forEach

`forEach()` 메서드는 주어진 함수를 배열 요소 각각에 대해 실행한다. 단순히 실행을 할뿐 **새로운 배열을 return 하지 않는다.** 

`forEach()` 를 통해 Local Storage에 저장을 하거나 API로 보내거나 경고를 보여주거나 하는 등의 기능을 할 수 있다. **단순 시행!!**

```javascript
const array1 = ['a', 'b', 'c'];

array1.forEach(element => console.log(element));

// expected output: "a"
// expected output: "b"
// expected output: "c"
```

[MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach)

## 4. Array.push

`push()` 메서드는 **배열의 끝에 하나 이상의 요소를 추가**하고, 배열의 새로운 길이를 반환한다. 

```javascript
const animals = ['pigs', 'goats', 'sheep'];

const count = animals.push('cows');
console.log(count);
// expected output: 4
console.log(animals);
// expected output: Array ["pigs", "goats", "sheep", "cows"]

animals.push('chickens', 'cats', 'dogs');
console.log(animals);
// expected output: Array ["pigs", "goats", "sheep", "cows", "chickens", "cats", "dogs"]
```

[MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/push)

## 5. Array.includes

**`includes()`** 메서드는 배열이 특정 요소를 포함하고 있는지 판별한다. 해당하는 string이 배열 안에 존재하는지 확인하는 메서드.

```javascript
const array1 = [1, 2, 3];

console.log(array1.includes(2));
// expected output: true

const pets = ['cat', 'dog', 'bat'];

console.log(pets.includes('cat'));
// expected output: true

console.log(pets.includes('at'));
// expected output: false
```

