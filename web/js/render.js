// data.js의 RESUME 객체를 DOM으로 렌더링하는 함수 모음.
// 데이터는 신뢰 가능한 로컬 파일이므로 innerHTML을 사용하되, 외부 입력은 받지 않는다.

const ICONS = {
  github:
    '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>',
  mail:
    '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 3h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zm0 1.5V5l6 3.5L14 5v-.5L8 8 2 4.5zM2 6.6V12h12V6.6L8 10 2 6.6z"/></svg>',
  phone:
    '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.65 1.33a1 1 0 0 1 1.16.4l1.4 2.1a1 1 0 0 1-.12 1.26l-.9.9a9.03 9.03 0 0 0 4.82 4.82l.9-.9a1 1 0 0 1 1.26-.12l2.1 1.4a1 1 0 0 1 .4 1.16l-.6 1.8a1 1 0 0 1-.95.69C7.1 14.84 1.16 8.9 1.16 1.88a1 1 0 0 1 .69-.95l1.8-.6z"/></svg>',
  file:
    '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 1h5l4 4v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zm5 1.5V5h2.5L9 2.5zM5 8h6v1.2H5V8zm0 2.5h6v1.2H5v-1.2z"/></svg>',
};

function el(tag, className, html) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (html !== undefined) node.innerHTML = html;
  return node;
}

function renderHero(root, profile, contact) {
  root.innerHTML = `
    <p class="hero__tag">// ${profile.title}</p>
    <h1 class="hero__name">${profile.name}</h1>
    <p class="hero__intro">${profile.intro}</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="${contact.github}" target="_blank" rel="noopener noreferrer">${ICONS.github} GitHub</a>
      <a class="btn" href="mailto:${contact.email}">${ICONS.mail} ${contact.email}</a>
      <a class="btn" href="tel:${contact.phone.replace(/-/g, '')}">${ICONS.phone} ${contact.phone}</a>
      <a class="btn" href="${profile.resumeFile}" download>${ICONS.file} 이력서 다운로드</a>
    </div>
  `;
}

function renderTimelineItem(item) {
  const card = el('article', 'tl-item');
  card.appendChild(el('div', 'tl-item__period', item.period));

  const body = el('div', 'tl-item__body');
  body.appendChild(el('div', 'tl-item__org', `[${item.org}]`));
  body.appendChild(el('h3', 'tl-item__title', item.title));

  const ul = el('ul', 'tl-item__bullets');
  item.bullets.forEach((b) => ul.appendChild(el('li', null, b)));
  body.appendChild(ul);

  if (item.techStack || item.github) {
    const footer = el('div', 'tl-item__footer');
    if (item.techStack) {
      const pills = el('div', 'pills');
      pills.appendChild(el('span', 'tech-label', 'Tech Stack'));
      item.techStack.forEach((t) => pills.appendChild(el('span', 'pill', t)));
      footer.appendChild(pills);
    }
    if (item.github) {
      const link = el('a', 'btn', `${ICONS.github} GitHub`);
      link.href = item.github;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      footer.appendChild(link);
    }
    body.appendChild(footer);
  }

  card.appendChild(body);
  return card;
}

function renderTimeline(root, items) {
  const wrap = el('div', 'timeline');
  items.forEach((item) => wrap.appendChild(renderTimelineItem(item)));
  root.replaceChildren(wrap);
}

function renderSkills(root, groups) {
  const wrap = el('div', 'skills');
  groups.forEach((g) => {
    const row = el('div', 'skill-group');
    row.appendChild(el('div', 'skill-group__name', g.category));
    const pills = el('div', 'pills');
    g.items.forEach((s) => pills.appendChild(el('span', 'pill', s)));
    row.appendChild(pills);
    wrap.appendChild(row);
  });
  root.replaceChildren(wrap);
}

function renderFooter(root, profile, contact) {
  root.innerHTML = `
    <div>© ${new Date().getFullYear()} ${profile.name}. All rights reserved.</div>
    <div class="footer__links">
      <a href="${contact.github}" target="_blank" rel="noopener noreferrer">GitHub</a>
      <a href="mailto:${contact.email}">${contact.email}</a>
      <a href="tel:${contact.phone.replace(/-/g, '')}">${contact.phone}</a>
    </div>
  `;
}

function renderAll(data) {
  renderHero(document.getElementById('hero-root'), data.profile, data.contact);
  renderTimeline(document.getElementById('education-root'), data.education);
  renderTimeline(document.getElementById('activities-root'), data.activities);
  renderSkills(document.getElementById('skills-root'), data.skills);
  renderTimeline(document.getElementById('projects-root'), data.projects);
  renderFooter(document.getElementById('footer-root'), data.profile, data.contact);
}
