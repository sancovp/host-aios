import type { Register } from 'claude-code'

// prompt-mirror — what Claude Code sends the model, mirrored into one YAML file per session, and changed by one
// control file the mod only reads. The design: ../../DESIGN.md.

// ─── YAML: the subset this mod writes (maps, lists, scalars, block text) and reads (maps, scalars, block text) ───

export type Tree = { [key: string]: string | Tree }

const SAFE_KEY = /^[A-Za-z0-9_-]+$/

function key(k: string): string {
  return SAFE_KEY.test(k) ? k : JSON.stringify(k)
}

function scalar(v: unknown): string {
  if (v === null || v === undefined) return 'null'
  if (typeof v === 'number' || typeof v === 'boolean') return String(v)
  return JSON.stringify(String(v))
}

// a block of text at `indent`: `|` keeps the final newline, `|-` has none; an indentation indicator when the first
// line starts with a space, so a reader does not take that space for the block's own indentation
function block(text: string, indent: number): string[] {
  const endsNewline = text.endsWith('\n')
  const body = endsNewline ? text.slice(0, -1) : text
  const lines = body.split('\n')
  const first = lines.find(l => l.trim() !== '') ?? ''
  const header = '|' + (/^\s/.test(first) ? '2' : '') + (endsNewline ? '' : '-')
  const pad = ' '.repeat(indent)
  return [header, ...lines.map(l => (l === '' ? '' : pad + l))]
}

function isMultiline(v: unknown): v is string {
  return typeof v === 'string' && (v.includes('\n') || v.length > 120)
}

function emitMap(obj: Record<string, unknown>, indent: number): string[] {
  const pad = ' '.repeat(indent)
  const out: string[] = []
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined) continue
    if (isMultiline(v)) {
      const [header, ...rest] = block(v, indent + 2)
      out.push(pad + key(k) + ': ' + header, ...rest)
    } else if (Array.isArray(v)) {
      if (v.length === 0) out.push(pad + key(k) + ': []')
      else {
        out.push(pad + key(k) + ':')
        for (const item of v) out.push(...emitItem(item, indent + 2))
      }
    } else if (v !== null && typeof v === 'object') {
      const entries = Object.keys(v as object)
      if (entries.length === 0) out.push(pad + key(k) + ': {}')
      else out.push(pad + key(k) + ':', ...emitMap(v as Record<string, unknown>, indent + 2))
    } else out.push(pad + key(k) + ': ' + scalar(v))
  }
  return out
}

function emitItem(item: unknown, indent: number): string[] {
  const pad = ' '.repeat(indent)
  if (item !== null && typeof item === 'object' && !Array.isArray(item)) {
    const lines = emitMap(item as Record<string, unknown>, indent + 2)
    if (lines.length === 0) return [pad + '- {}']
    lines[0] = pad + '- ' + (lines[0] ?? '').slice(indent + 2)
    return lines
  }
  if (isMultiline(item)) {
    const [header, ...rest] = block(item, indent + 2)
    return [pad + '- ' + header, ...rest]
  }
  return [pad + '- ' + scalar(item)]
}

export function toYaml(obj: Record<string, unknown>): string {
  return emitMap(obj, 0).join('\n') + '\n'
}

const KEY_LINE = /^("(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^\s:#'"][^:]*?)\s*:(?:\s+(.*))?$/

function unquoteKey(k: string): string {
  if (k.startsWith('"')) return JSON.parse(k)
  if (k.startsWith("'")) return k.slice(1, -1).replace(/''/g, "'")
  return k
}

function plainValue(rest: string, line: number): string {
  const dq = rest.match(/^("(?:[^"\\]|\\.)*")\s*(?:#.*)?$/)
  if (dq) return JSON.parse(dq[1] ?? '""')
  const sq = rest.match(/^'((?:[^']|'')*)'\s*(?:#.*)?$/)
  if (sq) return (sq[1] ?? '').replace(/''/g, "'")
  if (rest.startsWith('"') || rest.startsWith("'")) throw new Error('line ' + line + ': an unclosed quote')
  return rest.replace(/\s+#.*$/, '').trim()
}

// maps, scalars and block text — what a control file needs; anything else is refused with its line number
export function parseYaml(text: string): Tree {
  const lines = text.replace(/\r\n?/g, '\n').split('\n')
  const root: Tree = {}
  const stack: { indent: number; node: Tree }[] = [{ indent: -1, node: root }]
  let i = 0
  while (i < lines.length) {
    const raw = lines[i] ?? ''
    const trimmed = raw.trimStart()
    if (trimmed === '' || trimmed.startsWith('#')) {
      i++
      continue
    }
    const lead = raw.slice(0, raw.length - trimmed.length)
    if (lead.includes('\t')) throw new Error('line ' + (i + 1) + ': a tab in the indentation')
    const indent = lead.length
    const m = trimmed.match(KEY_LINE)
    if (!m) throw new Error('line ' + (i + 1) + ': expected "key: value", got ' + JSON.stringify(trimmed.slice(0, 60)))
    const k = unquoteKey(m[1] ?? '')
    const rest = (m[2] ?? '').trim()
    const top = (): { indent: number; node: Tree } => stack[stack.length - 1] ?? stack[0] ?? { indent: -1, node: root }
    while (stack.length > 1 && top().indent >= indent) stack.pop()
    const parent = top().node
    if (rest === '' || rest.startsWith('#')) {
      const child: Tree = {}
      parent[k] = child
      stack.push({ indent, node: child })
      i++
      continue
    }
    const b = rest.match(/^\|([+-]?)([1-9]?)([+-]?)\s*(?:#.*)?$/)
    if (b) {
      const chomp = b[1] || b[3]
      let content = b[2] ? indent + Number(b[2]) : -1
      i++
      const body: string[] = []
      while (i < lines.length) {
        const l = lines[i] ?? ''
        if (l.trim() === '') {
          body.push('')
          i++
          continue
        }
        const li = l.length - l.trimStart().length
        if (content === -1) {
          if (li <= indent) break
          content = li
        }
        if (li < content) break
        body.push(l.slice(content))
        i++
      }
      const trailing: string[] = []
      while (body.length > 0 && body[body.length - 1] === '') trailing.push(body.pop() as string)
      let value = body.join('\n')
      if (chomp === '+') value += '\n' + trailing.map(() => '\n').join('')
      else if (chomp !== '-' && body.length > 0) value += '\n'
      parent[k] = value
      continue
    }
    parent[k] = plainValue(rest, i + 1)
    i++
  }
  return root
}

// ─── THE CONTROL FILE: what to change in what is sent ───

export const DROP = 'drop'

export type Control = {
  system: Record<string, string>
  systemAppend?: string
  context: Record<string, string>
  attachments: Record<string, string>
  compactInstructions?: string
  compactAppend?: string
  compactRemove: Record<string, string> // a name → a sentence cut out of the rows a compaction stores
}

function textMap(tree: Tree, name: string, label: string = name): Record<string, string> {
  const node = tree[name]
  if (node === undefined) return {}
  if (typeof node === 'string') throw new Error('"' + label + '" must hold keys, one per thing to change')
  const out: Record<string, string> = {}
  for (const [k, v] of Object.entries(node)) {
    if (typeof v !== 'string') throw new Error('"' + label + '.' + k + '" must be text or drop')
    out[k] = v
  }
  return out
}

export function readControl(text: string): Control {
  const tree = parseYaml(text)
  const system = textMap(tree, 'system')
  const systemAppend = system['append']
  delete system['append']
  const compactNode = tree['compact']
  let compact: Tree = {}
  if (compactNode !== undefined) {
    if (typeof compactNode === 'string') throw new Error('"compact" must hold keys: instructions, append, remove')
    compact = compactNode
  }
  for (const [k, v] of Object.entries(compact)) {
    if (k === 'remove') continue
    if (k !== 'instructions' && k !== 'append') throw new Error('"compact.' + k + '" is not a key: instructions, append, remove')
    if (typeof v !== 'string') throw new Error('"compact.' + k + '" must be text')
  }
  return {
    system,
    systemAppend,
    context: textMap(tree, 'context'),
    attachments: textMap(tree, 'attachments'),
    compactInstructions: compact['instructions'] as string | undefined,
    compactAppend: compact['append'] as string | undefined,
    compactRemove: textMap(compact, 'remove', 'compact.remove'),
  }
}

export function countOverrides(c: Control): number {
  return (
    Object.keys(c.system).length +
    Object.keys(c.context).length +
    Object.keys(c.attachments).length +
    Object.keys(c.compactRemove).length +
    (c.systemAppend ? 1 : 0) +
    (c.compactInstructions !== undefined ? 1 : 0) +
    (c.compactAppend ? 1 : 0)
  )
}

// each named sentence cut out wherever it stands, its whitespace matched loosely (a line break where the file has a
// space still matches); what is left is closed up so no blank run remains where it stood
export function removeAll(text: string, removals: Record<string, string>): { text: string; removed: string[] } {
  const removed: string[] = []
  let out = text
  for (const [name, sentence] of Object.entries(removals)) {
    const words = sentence.trim()
    if (words === '') continue
    const pattern = new RegExp(words.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/\s+/g, '\\s+'), 'g')
    const next = out.replace(pattern, '')
    if (next !== out) {
      removed.push(name)
      out = next
    }
  }
  if (removed.length > 0) out = out.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n')
  return { text: out, removed }
}

const EMPTY: Control = { system: {}, context: {}, attachments: {}, compactRemove: {} }

export const TEMPLATE = `# prompt-mirror — THE CONTROL FILE. The mod reads it and never writes it; edit it while a session runs and the
# next request carries the change. What Claude Code sends, as it would send it, is in mirror.yaml beside this file.
#
# A value is text (a block: \`key: |\` then the text, indented) that replaces what is sent, or the word drop, which
# leaves it out. Keys come from mirror.yaml.
#
# system:                       # the system prompt, by section id
#   tone: drop
#   append: |                   # a section of your own, added last
#     ...
# context:                      # the first message's blocks: claudeMd (CLAUDE.md + the rules), userEmail, currentDate
#   currentDate: drop
# attachments:                  # each injected message, by its key in mirror.yaml
#   todo_reminder: drop
#   "hook:SessionStart": |      # a settings hook's injected text, by the hook's event
#     ...
# compact:                      # the compaction
#   instructions: |             # replaces what its summarizer is told (the /compact text included)
#     ...
#   append: |                   # added after what it is told
#     ...
#   remove:                     # sentences cut out of what it stores (the summary Claude Code injects), each named
#     a_name: |
#       the sentence, word for word as mirror.yaml shows it
`

// ─── THE CONTENT STEP: the host AIOS's boot config and rules, carried in this mod's own `content/` folder ───
// The host AIOS's build copies this mod into its package and writes `content/` beside it: `CLAUDE.md` (the boot
// config), `rules/<rule>` and `manifest.json` naming them. With it, the mod adds them to the instruction files a
// session's first message carries whenever those do not already hold the boot config — a session where nothing is
// installed — and adds nothing when they do. With no `content/` folder, as in prompt-mirror's own copy, it adds nothing.

export type Content = { root: string; boot: string; rules: { name: string; text: string }[] }

function squash(text: string): string {
  return text.replace(/\s+/g, ' ').trim()
}

// does what the session already loads hold the boot config?
export function holdsBoot(blocks: readonly { name: string; text: string }[], files: readonly { content?: string }[], boot: string): boolean {
  const want = squash(boot)
  if (want === '') return true
  const md = blocks.find(b => b.name === 'claudeMd')
  if (md && squash(md.text).includes(want)) return true
  return files.some(f => squash(String(f.content ?? '')).includes(want))
}

export function contentText(c: Content): string {
  const parts = [
    'Contents of ' + c.root + '/content/CLAUDE.md (the host AIOS boot config, carried by the host-aios-mod plugin because no installed folder loads it):\n\n' + c.boot,
    ...c.rules.map(r => 'Contents of ' + c.root + '/content/rules/' + r.name + ' (a host AIOS rule, carried by the host-aios-mod plugin):\n\n' + r.text),
  ]
  return parts.join('\n\n')
}

// the blocks with the content added: appended to the claudeMd block, or a claudeMd block of its own when there is none
export function addContent(blocks: { name: string; text: string }[], c: Content): { name: string; text: string }[] {
  const text = contentText(c)
  const at = blocks.findIndex(b => b.name === 'claudeMd')
  if (at === -1) return [{ name: 'claudeMd', text }, ...blocks]
  return blocks.map((b, i) => (i === at ? { ...b, text: (b.text ? b.text + '\n\n' : '') + text } : b))
}

let content: Content | null | undefined = undefined // undefined: not looked for yet · null: this copy carries none

async function loadContent($: any): Promise<Content | null> {
  if (content !== undefined) return content
  try {
    const root = String($.plugin.root ?? '').replace(/\/+$/, '')
    const manifest = JSON.parse(await $.fs.read(root + '/content/manifest.json'))
    const rules: { name: string; text: string }[] = []
    for (const name of manifest.rules ?? []) rules.push({ name: String(name), text: await $.fs.read(root + '/content/rules/' + name) })
    content = { root, boot: await $.fs.read(root + '/content/CLAUDE.md'), rules }
  } catch {
    content = null
  }
  return content
}

// ─── THE MIRROR: what was sent, kept in memory and written whole ───

type SectionRecord = { id: string; scope: string; sent: string; text: string }
type PromptRecord = { model: string; traits: string[]; renders: number; sections: SectionRecord[] }
type BlockRecord = { name: string; sent: string; text: string }
type AttachmentRecord = { key: string; type: string; origin: string; agent?: string; count: number; sent: string; text: string }
type CompactionRecord = {
  trigger: string
  agent?: string
  at: string
  instructions_received: string
  instructions_sent: string
  outcome: string
  tokens_before?: number
  tokens_after?: number
  messages: { role: string; tools: number; text: string }[]
  rows: { type: string; name?: string; removed: string[]; text: string }[] // what it stored, as stored
}

// one text, at most, in the mirror — a write over 4 MiB is refused, and the instruction files alone can run to
// hundreds of thousands of characters; what is cut is said, never silently dropped
const CAP = 1_000_000
const MESSAGE_CAP = 50_000 // each message a compaction leaves; the summary is the one that matters

function capped(text: string, cap: number = CAP): string {
  return text.length <= cap ? text : text.slice(0, cap) + '\n[prompt-mirror: ' + (text.length - cap) + ' more characters not mirrored]\n'
}

let dir = ''
let sessionId = ''
let control: Control = EMPTY
let controlError = ''
let controlMtime = -1
const prompts = new Map<string, PromptRecord>()
let contextFiles: string[] = []
let contextBlocks: BlockRecord[] = []
const attachments = new Map<string, AttachmentRecord>()
const compactions: CompactionRecord[] = []
let lastWritten = ''

function mirrorDoc(): Record<string, unknown> {
  return {
    note: 'Written by prompt-mirror; edits here are overwritten. To change what is sent, put the key in control.yaml.',
    session: sessionId,
    control: controlError ? 'NOT LOADED — ' + controlError : countOverrides(control) + ' override(s) loaded',
    system_prompts: [...prompts.values()],
    context: { files: contextFiles, blocks: contextBlocks },
    attachments: [...attachments.values()],
    compactions,
  }
}

async function writeMirror($: any): Promise<void> {
  if (!dir || !sessionId) return
  const text = toYaml(mirrorDoc())
  if (text === lastWritten) return
  lastWritten = text
  await $.fs.write(dir + '/mirror/' + sessionId + '.yaml', text)
  await $.fs.write(dir + '/mirror.yaml', text)
}

async function loadControl($: any): Promise<boolean> {
  const path = dir + '/control.yaml'
  let mtime = -1
  try {
    mtime = (await $.fs.stat(path)).mtimeMs
  } catch {
    mtime = -1
  }
  if (mtime === controlMtime) return false
  controlMtime = mtime
  if (mtime === -1) {
    control = EMPTY
    controlError = ''
    return true
  }
  try {
    control = readControl(await $.fs.read(path))
    controlError = ''
  } catch (error) {
    // a broken control file keeps the last good one in force and says why
    controlError = String((error as Error)?.message ?? error)
  }
  return true
}

function attachmentKey(e: any): string {
  const origin = e.origin ?? {}
  if (origin.kind === 'hook') return 'hook:' + String(origin.event ?? 'unknown')
  if (origin.kind === 'plugin') return 'plugin:' + String(origin.event ?? 'unknown')
  return String(e.type)
}

function summary(): string {
  const sections = [...prompts.values()].reduce((n, p) => n + p.sections.length, 0)
  return [
    'mirror:  ' + dir + '/mirror.yaml (this session: ' + dir + '/mirror/' + sessionId + '.yaml)',
    'control: ' + dir + '/control.yaml — ' + (controlError ? 'NOT LOADED: ' + controlError : countOverrides(control) + ' override(s)'),
    'seen:    ' + prompts.size + ' system prompt shape(s), ' + sections + ' section(s) · ' + contextBlocks.length +
      ' context block(s), ' + contextFiles.length + ' instruction file(s) · ' + attachments.size + ' attachment kind(s) · ' +
      compactions.length + ' compaction(s)',
  ].join('\n')
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    try {
      await $.command.register({ name: 'prompt-mirror', description: 'Show where the prompt mirror and its control file are, and what they hold' })
    } catch {
      // the command is a convenience; the mirror works without it
    }
    sessionId = await $.session.id()
    dir = ((await $.env.get('PROMPT_MIRROR_DIR')) || (await $.env.get('HOME')) + '/.claude/prompt-mirror').replace(/\/+$/, '')
    if (!(await $.fs.exists(dir + '/control.yaml'))) await $.fs.write(dir + '/control.yaml', TEMPLATE)
    await loadControl($)
    // the control file is re-read when it changes; only the cached answers whose part of it changed are asked again
    // (the system prompt is composed afresh every request, so it needs no asking)
    $.clock.every(2000, async () => {
      const before = control
      if (!(await loadControl($))) return
      if (JSON.stringify(before.context) !== JSON.stringify(control.context)) $.ui.invalidate('prompt.context')
      if (JSON.stringify(before.attachments) !== JSON.stringify(control.attachments)) $.ui.invalidate('prompt.attachment')
      $.ui.toast(controlError ? 'prompt-mirror: control.yaml NOT loaded — ' + controlError : 'prompt-mirror: control.yaml loaded — ' + countOverrides(control) + ' override(s)')
      await writeMirror($)
    })
    await writeMirror($)
    return next(e)
  }).catch(($, e, next) => next(e)) // the session starts whatever the mirror does

  on('command.run', { command: 'prompt-mirror' }, async () => ({ text: summary() }))

  // THE SYSTEM PROMPT — every section, as Claude Code composed it; a replaced or dropped one is marked
  on('prompt.compose', async ($, e, next) => {
    const composed = await next(e)
    const records: SectionRecord[] = []
    const sent: { id: string; text: string; scope: any }[] = []
    let changed = false
    for (const s of composed.sections) {
      const o = control.system[s.id]
      if (o === DROP) {
        records.push({ id: s.id, scope: s.scope, sent: 'dropped', text: capped(s.text) })
        changed = true
      } else if (o !== undefined) {
        records.push({ id: s.id, scope: s.scope, sent: 'replaced', text: capped(s.text) })
        sent.push({ ...s, text: o })
        changed = true
      } else {
        records.push({ id: s.id, scope: s.scope, sent: 'as is', text: capped(s.text) })
        sent.push(s)
      }
    }
    if (control.systemAppend) {
      sent.push({ id: 'prompt-mirror:append', text: control.systemAppend, scope: 'session' })
      records.push({ id: 'prompt-mirror:append', scope: 'session', sent: 'added', text: capped(control.systemAppend) })
      changed = true
    }
    const traits = [...(e.traits ?? [])].map(String)
    if (!traits.includes('analysis')) {
      const shape = e.promptModel + ' ' + traits.join(',') + ' ' + composed.sections.map(s => s.id).join(',')
      const prior = prompts.get(shape)
      prompts.set(shape, { model: e.promptModel, traits, renders: (prior?.renders ?? 0) + 1, sections: records })
      await writeMirror($)
    }
    // never an empty system prompt: an override that would leave none sends Claude Code's own
    if (!changed || sent.length === 0) return composed
    return { sections: sent }
  }).catch(($, e, next) => next(e))

  // THE FIRST MESSAGE'S CONTEXT — the instruction files (CLAUDE.md and the rules) as the claudeMd block, and the rest
  on('prompt.context', async ($, e, next) => {
    const got = await next(e)
    contextFiles = (e.instructionFiles ?? []).map((f: any) => String(f.path))
    // the content step first: the host AIOS's boot config and rules added when nothing the session loads holds them
    const carried = await loadContent($)
    const adding = carried !== null && !holdsBoot(got.blocks, e.instructionFiles ?? [], carried.boot)
    const blocks = adding ? addContent([...got.blocks], carried as Content) : got.blocks
    const out: { name: string; text: string }[] = []
    let changed = adding
    contextBlocks = blocks.map(b => {
      const o = control.context[b.name]
      if (o === DROP) {
        changed = true
        return { name: b.name, sent: 'dropped', text: capped(b.text) }
      }
      if (o !== undefined) {
        changed = true
        out.push({ ...b, text: o })
        return { name: b.name, sent: 'replaced', text: capped(b.text) }
      }
      out.push(b)
      return { name: b.name, sent: adding && b.name === 'claudeMd' ? 'content added' : 'as is', text: capped(b.text) }
    })
    if (adding) contextFiles = [...contextFiles, (carried as Content).root + '/content/CLAUDE.md', ...(carried as Content).rules.map(r => (carried as Content).root + '/content/rules/' + r.name)]
    await writeMirror($)
    return changed ? { blocks: out } : got
  }).catch(($, e, next) => next(e))

  // EVERY INJECTED MESSAGE — reminders, mode changes, mentioned files, a settings hook's output
  on('prompt.attachment', async ($, e, next) => {
    const got = await next(e)
    const k = attachmentKey(e)
    const o = control.attachments[k] ?? control.attachments[String(e.type)]
    const sent = o === DROP ? 'dropped' : o !== undefined ? 'replaced' : 'as is'
    const prior = attachments.get(k + ' ' + (e.agentId ?? ''))
    attachments.set(k + ' ' + (e.agentId ?? ''), {
      key: k,
      type: String(e.type),
      origin: String((e.origin as any)?.kind ?? 'engine'),
      agent: e.agentId,
      count: (prior?.count ?? 0) + 1,
      sent,
      text: capped(got.text ?? ''),
    })
    await writeMirror($)
    if (o === DROP) return { text: null }
    if (o !== undefined) return { text: o }
    return got
  }).catch(($, e, next) => next(e))

  // EACH COMPACTION — what the summarizer was told, and the conversation it left
  on('session.compact', async ($, e, next) => {
    const received = e.instructions ?? ''
    let told = received
    if (control.compactInstructions !== undefined) told = control.compactInstructions
    if (control.compactAppend) told = told ? told + '\n\n' + control.compactAppend : control.compactAppend
    const result: any = await next(told === received ? e : { ...e, instructions: told })
    compactions.push({
      trigger: String(e.trigger),
      agent: e.agentId,
      at: new Date(await $.clock.now()).toISOString(),
      instructions_received: received,
      instructions_sent: told,
      outcome: result.skip ? 'skipped — ' + String(result.skip) : 'compacted',
      tokens_before: result.tokensBefore,
      tokens_after: result.tokensAfter,
      messages: (result.messages ?? []).map((m: any) => ({ role: String(m.role), tools: (m.toolUses ?? []).length, text: capped(String(m.text ?? ''), MESSAGE_CAP) })),
      rows: [],
    })
    await writeMirror($)
    return result
  }).catch(($, e, next) => next(e))

  // WHAT A COMPACTION STORES — its boundary and its summary, the text Claude Code injects; the named sentences of
  // `compact.remove` are cut out here, where the row is kept, so every pinned field of the row stays Claude Code's
  on('session.append', async ($, e, next) => {
    if (e.door !== 'compaction') return next(e)
    const message: any = e.message
    const removed = new Set<string>()
    const cut = (t: string): string => {
      const r = removeAll(t, control.compactRemove)
      r.removed.forEach(n => removed.add(n))
      return r.text
    }
    const content =
      typeof message.content === 'string'
        ? cut(message.content)
        : (message.content ?? []).map((b: any) => (b?.type === 'text' && typeof b.text === 'string' ? { ...b, text: cut(b.text) } : b))
    const asText = typeof content === 'string' ? content : content.filter((b: any) => b?.type === 'text').map((b: any) => b.text).join('\n')
    let record = compactions[compactions.length - 1]
    if (!record) {
      record = { trigger: 'unseen', at: new Date(await $.clock.now()).toISOString(), instructions_received: '', instructions_sent: '', outcome: 'compacted', messages: [], rows: [] }
      compactions.push(record)
    }
    record.rows.push({ type: String(message.type), name: message.name, removed: [...removed], text: capped(asText, MESSAGE_CAP) })
    await writeMirror($)
    if (removed.size === 0) return next(e)
    return next({ ...e, message: { ...message, content } })
  }).catch(($, e, next) => next(e))
}
