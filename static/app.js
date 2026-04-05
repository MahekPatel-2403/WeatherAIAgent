document.addEventListener('DOMContentLoaded', ()=>{
  const input = document.getElementById('queryInput')
  const btn = document.getElementById('searchBtn')
  const searchResult = document.getElementById('searchResult')
  const place = document.getElementById('place')
  const weatherResult = document.getElementById('weatherResult')

  async function doQuery(q){
    const consoleEl = document.getElementById('agentConsole')
    searchResult.textContent = 'Searching...'
    place.textContent = ''
    weatherResult.textContent = ''
    consoleEl.textContent = ''
    try{
      const res = await fetch('/api/query',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body: JSON.stringify({query:q})
      })
      const data = await res.json()
      if(!res.ok){
        searchResult.textContent = data.error || 'Error'
        return
      }
      // Render console trace like modern agent UIs
      const trace = data.trace || []
      consoleEl.innerHTML = ''
      for(let i=0;i<trace.length;i++){
        const t = trace[i]
        const row = document.createElement('div')
        row.className = 'console-entry '+ (t.type || '')
        const left = document.createElement('div')
        left.className = 'console-icon'
        left.textContent = t.type ? t.type[0].toUpperCase() : '•'
        const right = document.createElement('div')
        right.className = 'console-body'
        const title = document.createElement('div')
        title.className = 'console-title'
        title.textContent = t.title
        const detail = document.createElement('div')
        detail.className = 'console-detail'
        detail.textContent = t.detail
        right.appendChild(title)
        right.appendChild(detail)
        row.appendChild(left)
        row.appendChild(right)
        // reveal entries with slight delay
        setTimeout(()=> consoleEl.appendChild(row), i*400)
      }

      // after console animation completes, populate results
      setTimeout(()=>{
        searchResult.textContent = data.search
        place.textContent = data.place
        weatherResult.textContent = JSON.stringify(data.weather, null, 2)
      }, Math.max(300, trace.length*400))
    }catch(err){
      searchResult.textContent = 'Request failed: '+err
    }
  }

  btn.addEventListener('click', ()=>{
    const q = input.value.trim()
    if(!q) return
    doQuery(q)
  })

  input.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') btn.click() })

  document.querySelectorAll('.chip').forEach(c=>{
    c.addEventListener('click', ()=>{
      input.value = c.dataset.q
      doQuery(c.dataset.q)
    })
  })
})
