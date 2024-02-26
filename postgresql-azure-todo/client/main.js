import { formDataToJson } from './utils.js';

document.querySelectorAll('nav button').forEach(button => {
  button.addEventListener('click', event => {
    document.querySelectorAll('.app-screen').forEach(screen => {
      if (
        screen.classList.contains(
          button.dataset.screen.toLowerCase() + '-screen'
        )
      ) {
        screen.classList.add('app-screen--active');
      } else {
        screen.classList.remove('app-screen--active');
      }
    });
  });
});

document.querySelectorAll('form').forEach(element => {
  element.addEventListener('submit', event => {
    event.preventDefault();
    var formData = new FormData(element);
    switch (element.id) {
      case 'signup-form':
        handleSignupForm(formData);
        break;

      case 'login-form':
        handleLoginForm(formData);
        break;

      case 'todo-form':
        handleTodoForm(formData);
        break;
    }
  });
});

async function handleTodoForm(formData) {
  await handleRequest(
    'http://127.0.0.1:3300/api/todo',
    formData,
    'Todo Success',
    'Todo Error'
  );
  if (data.success) {
    appendTodo(data.payload.todo);
  }
}

async function handleSignupForm(formData) {
  await handleRequest(
    'http://127.0.0.1:3300/api/signup',
    formData,
    'Signup Success',
    'Signup Error'
  );
}

async function handleLoginForm(formData) {
  await handleRequest(
    'http://127.0.0.1:3300/api/login',
    formData,
    'Login Success',
    'Login Error'
  );
}

async function handleRequest(url, formData, successMessage, errorMessage) {
  console.log(
    `[handle${successMessage.split(' ')[0]}Form] formData:`,
    formData
  );

  const jsonData = formDataToJson(formData);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(jsonData),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();

    if (data.success) {
      console.log(`${successMessage}:`, data);
    }
  } catch (error) {
    console.error(`${errorMessage}:`, error);
  }
}

function appendTodo(todo) {
  const div = document.createElement('div');
  div.textContent = todo;
  document.querySelector('.todo-container').appendChild(div);
}
