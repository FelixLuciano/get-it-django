function getRandomInt(min, max) {
  min = Math.ceil(min)
  max = Math.floor(max)

  return Math.floor(Math.random() * (max - min + 1)) + min
}

function debounce (callback, time) {
  let timeout;

  return function (...arguments) {
    clearTimeout(timeout)

    timeout = setTimeout(callback.bind(this, ...arguments), time)
  }
}

function getCookie (name) {
  const cookies = document.cookie.split(';')

  for (let cookie of cookies) {
    cookie = cookie.trim()

    const key = cookie.substring(0, name.length + 1)
    const value = cookie.substring(name.length + 1)

    if (key === name + '=') {
      return decodeURIComponent(value)
    }
  }
}


class Note {
  REQUEST_ENDPOINT = '/notes'

  constructor (node, tag) {
    if (node !== undefined) {
      this.node = node

      this.appendNode()
    } else {
      const template_node = document.querySelector('#js-note-card--template')
    
      this.node = template_node.content.firstElementChild.cloneNode(true)
    }

    if (tag !== undefined) {
      this.tag = tag
    }

    this.mountNode()
  }

  get titleInput_node () {
    return this.node.querySelector('.js-note-card__title')
  }

  get contentInput_node () {
    return this.node.querySelector('.js-note-card__content')
  }

  get peelButton_node () {
    return this.node.querySelector('.js-note-card__peel-button')
  }

  get removeButton_node () {
    return this.node.querySelector('.js-note-card__action-button--remove')
  }

  get tags () {
    const tagMatches = this.titleInput_node.innerText.match(/(?<=#)[^\s#]+/gm)

    if (tagMatches?.length > 0) {
      return new Set(tagMatches)
    }
    else {
      return new Set(['Notas'])
    }
  }
  set tag (value) {
    this.titleInput_node.innerText = `${value} ${this.titleInput_node.innerText}`
  }

  get note () {
    return {
      id: this.node.dataset.noteId,
      title: this.titleInput_node.innerText,
      content: this.contentInput_node.innerText,
      tags: Array.from(this.tags.values())
    }
  }

  set #id (value) {
    this.node.dataset.noteId = value
  }

  async fetchCreate () {
    const csrftoken = getCookie('csrftoken')

    const response = await fetch(this.REQUEST_ENDPOINT, {
      method: 'POST',
      body: JSON.stringify(this.note),
      headers: {
        'X-CSRFToken': csrftoken
      }
    })

    const data = (await response.json())[0]

    return {
      id: data.pk,
      ...data.fields
    }
  }

  fetchUpdate () {
    const csrftoken = getCookie('csrftoken')

    return fetch(this.REQUEST_ENDPOINT, {
      method: 'UPDATE',
      body: JSON.stringify(this.note),
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
  }

  fetchRemove () {
    const csrftoken = getCookie('csrftoken')

    return fetch(this.REQUEST_ENDPOINT, {
      method: 'DELETE',
      body: JSON.stringify(this.note),
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
  }

  appendNode () {
    document
      .querySelector('.js-notes-board__grid')
      .appendChild(this.node)
  }

  mountNode () {
    this.node.classList.add('note-card--color-' + getRandomInt(1, 5))
    this.node.classList.add('note-card--rotation-' + getRandomInt(1, 11))

    this.titleInput_node.addEventListener('input', debounce(() => this.fetchUpdate(), 1000))
    this.titleInput_node.addEventListener('keypress', (event) => {  
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        this.contentInput_node.focus()
      }
    })

    this.contentInput_node.addEventListener('input', debounce(() => this.fetchUpdate(), 1000))
    this.contentInput_node.addEventListener('keypress', (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {  
        event.preventDefault()
        this.contentInput_node.blur()
      }
    })

    this.peelButton_node.addEventListener('click', () => this.open())
    this.removeButton_node.addEventListener('click', () => this.remove())
  }

  open () {
    this.node.classList.add('js-note-card--open')

    window.addEventListener('click', this.close.bind(this))
  }

  close (event) {
    if (event !== undefined) {
      if (!event.path.includes(this.node)) {
        window.removeEventListener('click', this.close.bind(this))
        this.close()
      }
      else return
    }

    this.node.classList.remove('js-note-card--open')
  }

  focus () {
    const range = document.createRange()
    const selection = window.getSelection()

    range.selectNodeContents(this.titleInput_node)
    selection.removeAllRanges()
    selection.addRange(range)
  }

  async create () {
    const note = await this.fetchCreate()

    this.#id = note.id

    this.appendNode()
    this.focus()
  }

  async remove () {
    this.removeButton_node.disabled = true

    try {
      await this.fetchRemove()

      this.node.classList.remove('note-card--client-side')
      this.node.classList.add('note-card--remove-animation')

      this.node.addEventListener('animationend', () => this.node.remove())
    }
    finally {
      this.removeButton_node.disabled = false
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const noteCards_nodes = document.querySelectorAll('.js-note-card')
  const addNoteButton_node = document.querySelector('.js-button--add_note')

  for (const noteCard_node of noteCards_nodes) {
    new Note(noteCard_node)
  }

  addNoteButton_node?.addEventListener('click', async () => {
    const { tag } = addNoteButton_node.dataset

    const note = new Note(undefined, tag)

    addNoteButton_node.disabled = true

    try {
      await note.create()
    } finally {
      addNoteButton_node.disabled = false
    }
  })
})


class Tag extends Note {
  REQUEST_ENDPOINT = '/tags'

  constructor (node, tag) {
    super(node, tag)

    this.mountTagNode()
  }

  mountTagNode () {
    this.titleInput_node.addEventListener('input', () => {
      const tag = this.titleInput_node.innerText

      this.contentInput_node.querySelector('.js-tag-card__link').href = `/t/${tag}`
    }, 1000)
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const tagCards_nodes = document.querySelectorAll('.js-tag-card')
  const addTagButton_node = document.querySelector('.js-button--add_tag')

  for (const tagCard_node of tagCards_nodes) {
    new Tag(tagCard_node)
  }

  addTagButton_node?.addEventListener('click', async () => {
    const note = new Tag()

    addTagButton_node.disabled = true

    try {
      await note.create()
    } finally {
      addTagButton_node.disabled = false
    }
  })
})
