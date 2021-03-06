# 외부 API와 연동하여 뉴스 뷰어 만들기

지금까지 배운 내용들을 활용하여 카테고리별로 최신 뉴스 목록을 보여 주는 뉴스 뷰어 프로젝트를 진행해 보도록 하자.

Https://newsapi.org/에서 제공하는 API를 사용하여 데이터를 받아 오고, styled-component를 활용해 프로젝트를 스타일링할 예정이다. 이번 프로젝트는 다음과 같은 흐름으로 진행된다.

> 비동기 작업의 이해 → axios로 API 호출해서 데이터 받아오기 → newapi API 키 발급받기 → 뉴스 뷰어 UI 만들기 → 데이터 연동하기 → 카테고리 기능 구현하기 → 리액트 라우터 적용하기

## 14.1 비동기 작업의 이해

웹 패플리케이션을 만들다 보면 처리할 때 시간이 걸리는 작업이 있다. 예를 들어 웹 애플리케이션에서 서버 쪽 데이터가 필요할 때는 Ajax 기법을 사용하여 서버의 API를 호출함으로써 데이터를 수신한다. 이렇게 서버의 API를 사용해야 할 때는 네트워크 송수신 과정에서 시간이 걸리기 때문에 작업이 즉시 처리되는 것이 아니라, 응답을 받을 때까지 기다렸다가 전달받은 응답 데이터를 처리한다. 바로 이 과정에서 해당 작업을 비동기적으로 처리하게 된다.

![](https://media.vlpt.us/images/dek1313/post/67fcab43-5716-4d3f-bcb8-f4c8b6c91261/1.JPG)

만약 작업을 동기적으로 처리한다면 요청이 끝날 때까지 기다리는 동안 중지 상태가 되기 때문에 다른 작업을 할 수 없다. 해당 요청이 끝나야지만 다음 작업을 할 수가 있다. 이는 애플리케이션의 성능을 낮추고 자원을 낭비하는 현상을 발생시킬 수 있다. 하지만 이를 비동기적으로 처리한다면 웹 애플리케이션이 멈추지 않기 때문에 동시에 여러 가지 요청을 처리할 수도 있고, 기다리는 과정에서 다른 함수도 호출할 수 있다. 

이렇게 서버 API를 호출할 때 외에도 작업을 비동기적으로 처리할 때가 있는데, 바로 setTimeout 함수를 사용하여 특정 작업을 예약할 때이다. 예를 들어 다음 코드는 3초 후에 printMe함수를 호출한다.

```jsx
function printMe() {
  console.log('Hello World!');
}
setTimeout(printMe, 3000);
console.log('대기중...');
```

> -실행결과-
>
> 대기중...
>
> HelloWorld!

setTimeout이 사용되는 시점에서 코드가 3초 동안 멈추는 것이 아니라, 일단 코드가 위부터 아래까지 다 호출되고 3초 뒤에 우리가 지정해주 printMe함수가 호출되고 있다.

자바스크립트에서 비동기 작업을 할 때 가장 흔히 사용되는 방법이 콜백 함수를 사용하는 것이다. 위 코드에서 printMe가 3초 뒤에 호출되도록 printMe 함수 자체를 setTimeout 함수의 인자로 전달해 주었는데, 이런 함수를 콜백함수라고 부른다.

#### 14.1.1 콜백 함수

예를 들어 파라미터 값이 주어지면 1초 뒤에 10을 더해서 반환하는 함수가 있다고 생각해보자. 그리고 해당 함수가 처리된 직후 어떠한 작업을 하고 싶다면 다음과 같이 콜백 함수를 활용해서 작업한다.

```jsx
function increase(number, callback) {
  setTimeout(() => {
    const result = number + 10;
    if(callback) {
      callback(result);
    }
  },1000);
}

increase(0, result => {
  console.log(result);
});
```

1초에 걸쳐서 10, 20, 30, 40과 같은 형태로 여러 번 순차적으로 처리하고 싶다면 콜백 함수를 중첩하여 구현할 수 있다.

```jsx
function increase(number, callback) {
  setTimeout(() => {
    const result = number + 10;
    if(callback) {
      callback(result);
    }
  },1000);
}

console.log('작업 시작');
increase(0, result => {
  console.log(result);
  increase(result, result => {
  	console.log(result);
    increase(result, result => {
  		console.log(result);
      increase(result, result => {
  			console.log(result);
        increase(result, result => {
  			console.log(result);
        console.log('작업 완료');
});
```

> -실행 결과-
>
> 작업 시작
>
> 10
>
> 20
>
> 30
>
> 40
>
> 50
>
> 작업 완료

이렇게 콜백 안에 또 콜백을 넣어서 구현할 수 있는데, 여러 번 중첩되니까 코드의 가독성이 나빠졌다. 이러한 형태를 '콜백 지옥'이라고 부른다. 왠만하면 이러한 형태로 코드를 작성하는 것은 지양해야 된다. 

그렇다면 콜백 지옥을 만들지 않기 위한 방법으로는 어떤 방법이 있을까? 

자바스크립트에서 비동기적으로 처리하기 위한 방법으로 **Promise**, **async/await**가 있다

#### 14.1.2 Promise

Promise는 자바스크립트 ES6에 도입된 기능으로 콜백 지옥 같은 코드가 형성되지 않게 하는 방법이다. 앞에 작성한 코드를 Promise를 사용하여 구현해보자.

```jsx
function increase(number) {
	const promise = new Promise((resole, reject) => {
    // resolve는 성공, reject는 실패
    setTimeout(() => {
      const result = number + 10;
      if(result > 50) {
        // 50보다 높으면 에러 발생시키기
        const e = new Error('Number Too Big');
        return reject(e);
      }
      resolve(result); // number 값에 +10 후 성공 처리
    }, 1000);
  });
  return promise;
}

increase(0)
	.then(number => {
  	// Promise에서 resolve된 값은 .then을 통해 받아 올 수 있다.
  	console.log(number);
  	return increase(number); // Promise를 리턴하면
	})
	.then(number => {
  	console.log(number);
  	return increase(number);
	})
	.then(number => {
  	console.log(number);
  	return increase(number);
	})
	.then(number => {
  	console.log(number);
  	return increase(number);
	})
	.catch(e => {
  	// 도중에 에러가 발생한다면 .catch를 통해 알 수 있다.
  	console.log(e);
	})
```

여러 작업을 연달아 처리한다고 해서 함수를 여러 번 감싸는 것이 아니라 .then을 사용하여 그 다음 작업을 설정하기 때문에 콜백 지옥이 형성되지 않는다.

#### 14.1.3 async/await

async/await는 Promise를 더욱 쉽게 사용할 수 있도록 해 주는 ES2017(ES8) 문법이다. 이 문법을 사용하려면 함수의 앞부분에 async 키워드를 추가하고, 해당 함수 내부에서 Promise의 앞 부분에 await 키워드를 사용한다. 이렇게 하면 Promise가 끝날 때까지 기다리고, 결과 값을 특정 변수에 담을 수 있다.

```jsx
function increase(number) {
	const promise = new Promise((resole, reject) => {
    // resolve는 성공, reject는 실패
    setTimeout(() => {
      const result = number + 10;
      if(result > 50) {
        // 50보다 높으면 에러 발생시키기
        const e = new Error('Number Too Big');
        return reject(e);
      }
      resolve(result); // number 값에 +10 후 성공 처리
    }, 1000);
  });
  return promise;
}

async function runTasks() {
  // try/catch 구문을 사용하여 에러를 처리
  let result = await increase(0);
  try { 
    console.log(result)
    result = await increase(result);
    console.log(result)
    result = await increase(result);
    console.log(result)
    result = await increase(result);
    console.log(result)
    result = await increase(result);
    console.log(result)
    result = await increase(result);
    console.lgo(result);
  } catch(e) {
    console.log(e);
  }
}
```

## 14.2 axios로 API 호출해서 데이터 받아 오기

axios는 현재 가장 많이 사용되고 있는 자바스크립트 HTTP 클라이언트다. 이 라이브러리의 특징은 HTTP 요철을 Promise 기반으로 처리한다는 점이다. 리액트 프로젝트를 생성하여 이 라이브러리를 설치하고 사용하는 방법을 알아보도록 하자.

`$ yarn create react-app news-viewer`

`$ yarn add axios`

설치를 다 마친 후 App.js의 코드를 다음과 같이 고쳐줬다.

```jsx
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const onClick = () => {
    axios
      .get("https://jsonplaceholder.typicode.com/todos/1")
      .then((response) => {
        setData(response.data);
      });
  };
  return (
    <div>
      <div>
        <button onClick={onClick}>불러오기</button>
      </div>
      {data && (
        <textarea
          rows={7}
          value={JSON.stringify(data, null, 2)}
          readOnly={true}
        />
      )}
    </div>
  );
}

export default App;
```

위 코드는 **불러오기** 버튼을 누르면 JSONPlaceholder에서 제공하는 가짜 API를 호출하고 이에 대한 응답을 컴포넌트 상태에 넣어서 보여주는 예제다.

<img src="./images/14_01.png" />

onClick 함수에서 axios.get 함수를 사용했다. 이 함수는 파라미터로 전달된 주소에 GET 요청을 해준다. 그리고 이에 대한 결과는 .then을 통해 비동기적으로 확인할 수 있다. 위 코드에 async를 적용하려면 아래와 같이 코드를 수정해주면 된다.

```jsx
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const onClick = async () => {
    try{
    	const response = await axios.get("https://jsonplaceholder.typicode.com/todos/1")  
      setData(response.data);
    } catch(e) {
      console.log(e)
    }
  };
  return (
    <div>
      <div>
        <button onClick={onClick}>불러오기</button>
      </div>
      {data && (
        <textarea
          rows={7}
          value={JSON.stringify(data, null, 2)}
          readOnly={true}
        />
      )}
    </div>
  );
}

export default App;
```

화살표 함수에 async/await를 적용할 때는 async () => {} 와 같은 형식으로 적용한다. 불러오기 버튼을 눌렀을 때 이전과 같이 데이터를 잘 받아오는 것을 확인할 수 있다.

## 14.3 newsapi API 키 발급 받기

이번 프로젝트에서는 newsapi에서 제공하는 API를 사용하여 최신 뉴스를 불러온 후 보여 줄 것이다. 이를 수행하기 위해선 사전에 newsapi에서 API 키를 발급받아야 한다. API 키는 https://newsapi.org/register에 가입하면 발급받을 수 있다. 

7f503bc4b6d64e3baa9f7b4593d8e279

API 키는 외부에 노출시키지 않는 것이 좋은데 만약에 나의 API 키를 사용해서 API를 요청하는 사람들이 많다고 가정한다면 사이트 측에서 block을 걸어 버릴 수도 있다. 그렇기에 API키는 나만 알 수 있는 곳에 안전하게 저장을 해두는 습관이 필요하다.

발급받은 API 키는 추후 API를 요청할 때 API 주소의 쿼리 파라미터로 넣어서 사용하면 된다. 우리가 사용할 API에 대해서 알아보자. https://newsapi.org/s/south-korea-news-api 링크에 들어가면 한국 뉴스를 가져오는 API에 대한 설명서가 있다.

사용할 API 주소는 두 가지 형태다.

1. 전체 뉴스 불러오기

   GET https://newsapi.org/v2/top-headlines?country=kr&apiKey=7f503bc4b6d64e3baa9f7b4593d8e279

2. 특정 카테고리 뉴스 불러오기

   GET https://newsapi.org/v2/top-headlines?country=kr&category=technology&apiKey=7f503bc4b6d64e3baa9f7b4593d8e279

이제 기존 리액트 프로젝트에서 사용해던 JSONPlacholder 가짜 API를 전체 뉴스를 불러오는 API로 대체하면 다음과 같이 전체 뉴스를 정상적으로 불러오는 것을 확인할 수 있다.

<img src="./images/14_02.png" />

## 14.4 뉴스 뷰어 UI 만들기

styled-Component를 사용하여 뉴스 정보를 보여 줄 컴포넌트를 만들어 보자

Src 디렉터리 안에 components를 만들고 그 안에 NewsItem.js와 NewsList.js 파일을 만들어 준다. NewsItem은 각 뉴스 정보를 보여 주는 컴포넌트이고, NewsList는 API를 요청하고 뉴스 데이터가 들어 있는 배열을 컴포넌트 배열로 변환하여 렌더링해 주는 컴포넌트다.

#### 14.4.1 NewsItem

NewsItem을 만들기 전에 각 뉴스 데이터에 어떤 필드가 있는지 확인해보는 것이 필요하다. 위의 첨부된 이미지를 보면 전체 뉴스 API를 호출했을 때 받아오는 JSON 데이터인데 내가 사용할 데이터는 아래와 같다.

- title: 제목
- description: 내용
- url: 링크
- urlToImage: 뉴스 이미지

NewsItem 컴포넌트는 article이라는 객체를 props로. 통째로 받아 와서 사용한다. NewsItem 컴포넌트를 아래와 같이 작성해줬다.

```jsx
import React from "react";
import styled from "styled-components";

const NewItemBlock = styled.div`
  display: flex;
  .thumbnail {
    margin-right: 1rem;
    img {
      display: block;
      width: 160px;
      height: 100px;
      object-fit: cover;
    }
  }
  .contents {
    h2 {
      margin: 0;
      a {
        color: black;
      }
    }
    p {
      margin: 0;
      line-height: 1.5;
      margin-top: 0.5rem;
      white-space: normal;
    }
  }
  & + & {
    margin-top: 3rem;
  }
`;

const NewsItem = ({ article }) => {
  const { title, description, url, urlToImage } = article;
  return (
    <NewItemBlock>
      {urlToImage && (
        <div className="thumbnail">
          <a href={url} target="_blank" rel="noopener noreferrer">
            <img src={urlToImage} atl="thumbnail" />
          </a>
        </div>
      )}
      <div className="contents">
        <h2>
          <a href={url} target="_blank" rel="noopener noreferrer">
            {title}
          </a>
        </h2>
        <p>{description}</p>
      </div>
    </NewItemBlock>
  );
};

export default NewsItem;
```

#### 14.4.2 NewsList

이 컴포넌트에서 API 요청을 하게 될텐데 아직 데이터를 불러오지 않고 있으니 sampleArticle이라는 객체에 미리 예시 데이터(Mock Data)를 넣은 후 각 컴포넌트에 전달하여 가짜 내용을 보이게 해줬다.

```jsx
import React from "react";
import styled from "styled-components";
import NewsItem from "./NewsItem";

const NewsListBlock = styled.div`
  box-sizing: border-box;
  padding-bottom: 3rem;
  width: 768px;
  margin: 0 auto;
  margin-top: 2rem;
  @media screen and (max-width: 768px) {
    width: 100%;
    padding-left: 1rem;
    padding-right: 1rem;
  }
`;

const sampleArticle = {
  title: "제목",
  description: "내용",
  url: "https://google.com",
  urlToImage: "https://via.placeholder.com/160",
};

const NewsList = () => {
  return (
    <NewsListBlock>
      <NewsItem article={sampleArticle} />
      <NewsItem article={sampleArticle} />
      <NewsItem article={sampleArticle} />
      <NewsItem article={sampleArticle} />
      <NewsItem article={sampleArticle} />
      <NewsItem article={sampleArticle} />
      <NewsItem article={sampleArticle} />
      <NewsItem article={sampleArticle} />
    </NewsListBlock>
  );
};

export default NewsList;
```

그런 다음 App 컴포넌트를 다 지우고 NewsList를 렌더링 해주면 다음과 같은 화면이 나타나게 된다.

<img src="./images/14_03.png" />

## 14.5 데이터 연동하기

NewsList 컴포넌트에서 이전에 연습 삼아 사용했던 API를 호출해 보도록 하자. 컴포넌트가 화면에 보이는 시점에 API를 요청하게 될텐데, useEffect를 사용해서 컴포넌트가 처음 렌더링되는 시점에 API를 요청하면 된다. 여기서 주의할 점은 useEffect에 등록하는 함수에 async를 붙이면 안된다는 것이다. useEffect에서 반환해야 하는 값은 뒷정리 함수이기 때문이다. 따라서 내부에서 async/await를 사용하고 싶다면, 함수 내부에 async 키워드가 붙은 또다른 함수를 만들어서 사용해줘야 한다.

 추가로 loading이라는 state도 관리해서 API요청이 대기 중인지 판별하도록 할 것이다. 요청이 대기 중일때는 true, 요청이 끝나면 false가 되어야 한다.

```jsx
import React, { useEffect, useState } from "react";
import styled from "styled-components";
import NewsItem from "./NewsItem";
import axios from "axios";

const NewsListBlock = styled.div`
  box-sizing: border-box;
  padding-bottom: 3rem;
  width: 768px;
  margin: 0 auto;
  margin-top: 2rem;
  @media screen and (max-width: 768px) {
    width: 100%;
    padding-left: 1rem;
    padding-right: 1rem;
  }
`;

const NewsList = () => {
  const [articles, setArticles] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // async를 사용하는 함수 따로 선언
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(
          "https://newsapi.org/v2/top-headlines?country=kr&apiKey=7f503bc4b6d64e3baa9f7b4593d8e279"
        );
        setArticles(response.data.articles);
      } catch (e) {
        console.log(e);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  // 대기 중일 때
  if (loading) {
    return <NewsListBlock>대기 중...</NewsListBlock>;
  }
  // Articles 값이 설정되지 않았을 때
  if (!articles) {
    return null;
  }

  return (
    <NewsListBlock>
      {articles.map((article) => (
        <NewsItem article={article} />
      ))}
    </NewsListBlock>
  );
};

export default NewsList;
```

데이터를 불러와서 뉴스 데이터 배열을 map 함수를 이요해서 컴포넌트 배열로 변활할 때 신경 써야 할 부분이 있다. Map 함수를 사용하기 전에 꼭 !articles를 조회하여 해당 값이 현재 null이 아닌지 검사해야 한다. 이 작업을 하지 않으면, 아직 데이터가 없을 때 null 에는 map 함수가 없기 때문에 렌더링 과정에서 오류가 발생하고 화면에는 흰 페이지만 나오게 된다.

저장하고 화면을 보면 정상적으로 뉴스 데이터를 받아와 화면에서 출력하는 것을 볼 수 있다.

<img src="./images/14_04.png" />

## 14.6 카테고리 기능 구현

뉴스의 카테고리는 총 6개이며 다음과 같이 영어로 되어 있다.

- Business(비즈니스) 	
- Science(과학)
- Entertainment(연예) 
- Sports(스포츠)
- Health(건강)
- Technology(기술)

화면에 카테고리를 보여 줄 때는 영어로 된 값을 그대로 보여 주지 않고, 한글로 보여 준 뒤 클릭했을 때 영어로 된 카테고리 값을 사용하도록 구현할 예정이다.

#### 14.6.1 카테고리 선택 UI 만들기

Categories.js 파일을 만들어 다음과 같이 작성해준다.

```jsx
import React from "react";
import styled from "styled-components";

const categories = [
  {
    name: "all",
    text: "전체보기",
  },
  {
    name: "busniess",
    text: "비즈니스",
  },
  {
    name: "entertainment",
    text: "엔터테인먼트",
  },
  {
    name: "health",
    text: "건강",
  },
  {
    name: "science",
    text: "과학",
  },
  {
    name: "sports",
    text: "스포츠",
  },
  {
    name: "technology",
    text: "기술",
  },
];

const CategoriesBlock = styled.div`
  display: flex;
  padding: 1rem;
  width: 768px;
  margin: 0 auto;
  @media screen and (max-width: 768px) {
    width: 100%;
    overflow-x: auto;
  }
`;

const Category = styled.div`
  font-size: 1.125rem;
  cursor: pointer;
  white-space: pre;
  text-decoration: none;
  color: inherit;
  padding-bottom: 0.25rem;

  &:hover {
    color: #495057;
  }

  & + & {
    margin-left: 1rem;
  }
`;

const Categories = () => {
  return (
    <CategoriesBlock>
      {categories.map((category) => (
        <Categogy key={category.name}>{category.text}</Categogy>
      ))}
    </CategoriesBlock>
  );
};

export default Categories;
```

위 코드에서는 categories라는 배열 안에 name과 text 값이 들어가 있는 객체들을 넣어 주어서 한글로 된 카테고리와 실제 카테고리 값을 연결시켜 주었다. 여기서 name은 실제 카테고리 값을 가리키고, text 값은 렌더링할 때 사용할 카테고리를 가리킨다.

다 만든 컴포넌트는 App에서 NewList 컴포넌트 상단에 렌더링 시켜준다. 저장 후 화면을 보면 아래와 같이 카테고리가 상단에 잘 나타나는 것을 확인할 수 있다.

<img src="./images/14_05.png" />

이제 App에서 category 상태를 useState로 관리해보자. 추가로 category 값을 업데이는 하는 onSelect라는 함수도 만들어 준다. 그러고 나서 category와 onSelect 함수를 Categories 컴포넌트에게 props로 전달해준다. 또한 category 값을 NewsList 컴포넌트에게도 props로 전달해준다.

```jsx
import React, { useCallback, useState } from "react";
import Categories from "./components/Categories";
import NewsList from "./components/NewsList";

function App() {
  const [category, setCategory] = useState("all");
  const onSelect = useCallback((category) => setCategory(category), []);
  return (
    <>
      <Categories category={category} onSelect={onSelect} />
      <NewsList category={category} />
    </>
  );
}

export default App;
```

다음으로 Categories에서는 props로 전달받은 onSelect를 각 Category 컴포넌트의 onClick으로 설정해 주고, 현재 선택된 카테고리 값에 따라 다른 스타일을 적용해보도록 하자.

```jsx
import React from "react";
import styled, { css } from "styled-components";

const categories = [
  {
    name: "all",
    text: "전체보기",
  },
  {
    name: "busniess",
    text: "비즈니스",
  },
  {
    name: "entertainment",
    text: "엔터테인먼트",
  },
  {
    name: "health",
    text: "건강",
  },
  {
    name: "science",
    text: "과학",
  },
  {
    name: "sports",
    text: "스포츠",
  },
  {
    name: "technology",
    text: "기술",
  },
];

const CategoriesBlock = styled.div`
  display: flex;
  padding: 1rem;
  width: 768px;
  margin: 0 auto;
  @media screen and (max-width: 768px) {
    width: 100%;
    overflow-x: auto;
  }
`;

const Category = styled.div`
  font-size: 1.125rem;
  cursor: pointer;
  white-space: pre;
  text-decoration: none;
  color: inherit;
  padding-bottom: 0.25rem;

  &:hover {
    color: #495057;
  }

  ${(props) =>
    props.active &&
    css`
      font-weight: 600;
      border-bottom: 2px solid #22b8cf;
      color: #22b8cf;
      &:hover {
        color: #3bc9db;
      }
    `}

  & + & {
    margin-left: 1rem;
  }
`;

const Categories = ({ category, onSelect }) => {
  return (
    <CategoriesBlock>
      {categories.map((c) => (
        <Category
          key={c.name}
          onClick={() => onSelect(c.name)}
          active={category === c.name}
        >
          {c.text}
        </Category>
      ))}
    </CategoriesBlock>
  );
};

export default Categories;
```

저장후 화면을 보게 되면 다음과 같이 청록색의 스타일이 선택된 카테고리에 입혀진 것을 확인할 수 있다.

<img src="./images/14_06.png" />

#### 14.6.2 API를 호출할 때 카테고리 지정하기

현재는 API를 요청할 때 전체 뉴스 목록을 불러오는 것만 구현이 되어 있지만 카테고리를 눌렀을 때 해당 카테고리에 맞는 뉴스들을 불러올 수 있도록 NewsList 컴포넌트에서 현재 props로 받아 온 category에 따라 API를 요청하도록 구현해보도록 하자.

```jsx
import React, { useEffect, useState } from "react";
import styled from "styled-components";
import NewsItem from "./NewsItem";
import axios from "axios";

(...)
 
const NewsList = ({ category }) => {
  const [articles, setArticles] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // async를 사용하는 함수 따로 선언
    const fetchData = async () => {
      setLoading(true);
      try {
        const query = category === "all" ? "" : `&category=${category}`;
        const response = await axios.get(
          `https://newsapi.org/v2/top-headlines?country=kr${query}&apiKey=7f503bc4b6d64e3baa9f7b4593d8e279`
        );
        setArticles(response.data.articles);
      } catch (e) {
        console.log(e);
      }
      setLoading(false);
    };
    fetchData();
  }, [category]);

  // 대기 중일 때
  if (loading) {
    return <NewsListBlock>대기 중...</NewsListBlock>;
  }
  // Articles 값이 설정되지 않았을 때
  if (!articles) {
    return null;
  }

  return (
    <NewsListBlock>
      {articles.map((article) => (
        <NewsItem article={article} />
      ))}
    </NewsListBlock>
  );
};

export default NewsList;
```

현재 category 값이 무엇인지에 따라 요청할 주소가 동적으로 바뀌고 있다. category 값이 'all'이라면 query 값을 공백으로 설정하고, 'all'이 아니라면 "&category=카테고리" 형태의 문자열을 만들도록 했다. 그리고 이 query를 요청할 때 주소에 포함시켜 줬다.

추가로 category 값이 바뀔 때마다 뉴스를 새로 불러와야 하기 때문에 useEffect의 의존 배열(두 번째 파라미터로 설정하는 배열)에 category를 넣어 주어야 한다. 만약 이 컴포넌트를 클래스형 컴포넌트로 만들게 된다면 componentDidMount와 componentDidUpdate에서 요청을 하도록 설정해 주어야 하는데 함수형 컴포넌트라면 useEffect 한 번으로 컴포넌트가 맨 처음 렌더링될 때, category 값이 바뀔 때 요청하도록 설정해 줄 수 있다.

저장 후 브라우저를 열어 다른 카테고리를 눌러보면 해당 카테고리에 따른 기사들을 정상적으로 불러오는 것을 확인할 수 있다.

<img src="./images/14_07.png" />

## 14.7 리액트 라우터 적용

뉴스 뷰어 프로젝트에 리액트 라우터를 적용해보자. 기존에는 카테고리 값을 useState로 관리 했는데 이번에는 이 값을 리액트 라우터의 URL 파라미터를 사용하여 관리해보겠다.

우선 리액트 라우터를 설치하고 index.js에서 리액트 라우터를 적용시켜 준다.

#### 14.7.1 NewsPage

이번 실습에서 리액트 라우터를 적용할 때 만들어야 할 페이지는 단 하나다. src 디렉터리에 pages라는 디렉터리를 생성하고 NewsPages.js 파일을 만들어 아래와 같이 작성해 준다.

```jsx
import React from "react";
import Categories from "../components/Categories";
import NewsList from "../components/NewsList";

const NewsPage = ({ match }) => {
  // 카테고리가 선택되지 않았으면 기본값 all로 사용
  const category = match.params.category || "all";

  return (
    <>
      <Categories />
      <NewsList category={category} />
    </>
  );
};

export default NewsPage;
```

현재 선택된 category 값을 URL 파라미터를 통해 사용할 것이므로 Categories 컴포넌트에서 현재 선택된 카테고리 값을 알려 줄 필요도 없고, onSelect 함수를 따로 전달해 줄 필요도 없다. App컴포넌트의 기존 내용을 다 지우고 Route를 정의 해준다.

```jsx
import React from "react";
import { Route } from "react-router-dom";
import NewsPage from "./pages/NewsPage";

function App() {
  return <Route path="/:category?" component={NewsPage} />;
}

export default App;
```

위 코드에서 사용된 path에 `/:category?` 와 같은 형태로 맨 뒤에 물음표 문자가 들어가 있다. 이는 category 값이 선택적(optional)이라는 의미다. 즉, 있을 수도 있고 없을 수도 있다는 뜻이다. 만약 category URL 파라미터가 없다면 전체 카테고리를 선택한 것으로 간주한다.

#### 14.7.2 Categories에서 NavLink 사용

이제 Categories에서 기존의 onSelect 함수를 호출하여 카테고리를 선택하고, 선택된 카테고리에 다른 스타일을 주는 기능을 NavLink로 대체 해보도록 하자. div, button, input 처럼 일반 HTML 요소가 아닌 특정 컴포넌트에 styled-components를 사용하려면 **styled(컴포넌트이름)``** 같은 형식을 사용한다.

```jsx
import React from "react";
import { NavLink } from "react-router-dom";
import styled from "styled-components";

const categories = [
	(...)
];

const CategoriesBlock = styled.div`
	(...)
`;

const Category = styled(NavLink)`
  font-size: 1.125rem;
  cursor: pointer;
  white-space: pre;
  text-decoration: none;
  color: inherit;
  padding-bottom: 0.25rem;

  &:hover {
    color: #495057;
  }

  &.active {
    font-weight: 600;
    border-bottom: 2px solid #22b8cf;
    color: #22b8cf;
    &:hover {
      color: #3bc9db;
    }
  }

  & + & {
    margin-left: 1rem;
  }
`;

const Categories = () => {
  return (
    <CategoriesBlock>
      {categories.map((c) => (
        <Category
          key={c.name}
          activeClassName="active"
          exact={c.name === "all"}
          to={c.name === "all" ? "/" : `/${c.name}`}
        >
          {c.text}
        </Category>
      ))}
    </CategoriesBlock>
  );
};

export default Categories;
```

NavLink로 만들어진 Category 컴포넌트에 to 값은 "/카테고리이름" 으로 설정해줬다. 그리고 카테고리 중에서 **전체보기** 같은 경우 예외적으로 "/all" 대신 "/"로 설정했다. to 값이 "/"를 가리키고 있을 때는 exact 값도 true로 해줘야 한다. 이 값을 설정하지 않으면 다른 카테고리가 선택됐을 때도 전체보기 링크에 active 스타일이 적용되는 오류가 발생한다.

저장한 후 브라우저를 확인하면 카테고리에 따라 URL이 바뀌고 뉴스 데이터도 정상적으로 출력되는 것을 확인할 수 있다.

<img src="./images/14_08.png" />

## 14.8 usePromise 커스텀 Hooks 만들기

이번에는 컴포넌트에서 API 호출처럼 Promise를 사용해야 하는 경우 더욱 간결하게 코드를 작성할 수 있도록 해 주는 커스텀 Hooks를 만들어서 프로젝트에 적용시켜 보자.

만들 Hook의 이름은 usePromise다. Src 디렉터리에 lib 디렉터리를 만들고, 그 안에 usePromise.js를 아래와 같이 작성해준다.

```jsx
import { useState, useEffect } from "react";

export default function usePromise(promiseCreator, deps) {
  // 대기중/완료/실패에 대한 상태 관리
  const [loading, setLoading] = useState(false);
  const [resolved, setResolved] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const process = async () => {
      setLoading(true);
      try {
        const resolved = await promiseCreator();
        setResolved(resolved);
      } catch (e) {
        setError(e);
      }
      setLoading(false);
    };
    process();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return [loading, resolved, error];
}
```

프로젝트의 다양한 곳에서 사용될 수 있는 유틸 함수들은 보통 이렇게 src 디렉터리에 lib 디렉터리를 만든 후 그 안에 작성한다. 방금 만든 usePromise Hook은 Promise의 대기 중, 완료 결과, 실패 결과에 대한 상태를 관리하며, usePromise의 의존 배열 deps를 파라미터로 받아 온다. 파라미터로 받아 온 deps 배열은 usePromise 내부에서 사용한 useEffect의 의존 배열로 설정되는데 이 배열을 설정하는 부분에서 ESLint 경고가 나타나게 된다.

이 경고를 무시하려면 특정 줄에서만 ESLint 규칙을 무시하도록 주석을 작성해야 한다. 에디터에 초록색 경고 줄이 그어졌을 때 그 위에 커서를 올리면 **빠른 수정**... 이라는 문구가 나타나는데, 이를 클릭하면 자동으로 ESLint 규칙을 비활성화 시키는 주석을 입력할 수 있다.

코드를 저장한 뒤 NewsList 컴포넌트에서 usePromise를 사용해보자.

```jsx
import React from "react";
import styled from "styled-components";
import NewsItem from "./NewsItem";
import axios from "axios";
import usePromise from "../lib/usePromise";

const NewsListBlock = styled.div`
	(...)
`;

const NewsList = ({ category }) => {
  const [loading, response, error] = usePromise(() => {
    const query = category === "all" ? "" : `&category=${category}`;
    return axios.get(
      `https://newsapi.org/v2/top-headlines?country=kr${query}&apiKey=7f503bc4b6d64e3baa9f7b4593d8e279`
    );
  }, [category]);

  // 대기 중일 때
  if (loading) {
    return <NewsListBlock>대기 중...</NewsListBlock>;
  }
  // 아직 reponse 값이 설정되지 않았을 때
  if (!response) {
    return null;
  }
  // 에러가 발생했을 때
  if (error) {
    return <NewsListBlock>에러 발생!</NewsListBlock>;
  }

  // reponse 값이 유효할 때
  const { articles } = response.data;

  return (
    <NewsListBlock>
      {articles.map((article) => (
        <NewsItem article={article} />
      ))}
    </NewsListBlock>
  );
};

export default NewsList;
```

usePromise를 사용하면 NewsList에서 대기 중 상태 관리와 useEffect 설정을 직접 하지 않아도되므로 코드가 훨씬 간결해진다. 요청 상태를 관리할 때 무조건 커스텀 Hook을 만들어서 사용해야 하는 것은 아니지만, 상황에 따라 적절히 사용하면 좋은 코드를 만들어 갈 수 있다.

## 14.9 정리

이 장에서는 외부 API를 연동하여 사용하는 방법을 알아보고, 지금까지 배운 것을 활용하여 실제로 쓸모 있는 프로젝트를 개발해 봤다. 리액트 컴포넌트에서 API를 연동하여 개발할 때 절대 잊지 말아야 할 유의 사항은 useEffect에 등록하는 함수는 async로 작성하면 안된다는 점이다. 그 대신에 함수 내부에 async 함수를 따로 만들어 주어야 한다.

지금은 usePromise라는 커스텀 Hook을 만들어 사용함으로써 코드가 조금 간결해지기는 했지만, 나중에 사용해야 할 API의 종류가 많아지면 요청을 위한 상태 관리를 하는 것이 번거로워질 수 있다. 뒤에 나올 리덕스와 리덕스 미들웨어를 배우면 좀 더 쉽게 요청에 대한 상태 관리를 할 수 있다.

