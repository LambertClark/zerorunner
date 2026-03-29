export interface TStepDataStat {
  id?: number | null
  name: string
  case_id?: number | null
  enable: boolean
  index: number
  step_type: string
  variables?: any[]
  setup_hooks?: any[]
  teardown_hooks?: any[]
  extracts?: ExtractData[]
  export?: any[]
  validators?: ValidatorData[]
  request?: TRequestData | Record<string, any>
  sql_request?: TSqlRequest
  loop_request?: TStepLoopData
  if_request?: TStepIFData
  wait_request?: TStepWaitData
  script_request?: TStepScriptData
  ui_request?: TUiRequestData
  showDetail?: boolean
}

export interface ExtractData {
  name: string
  path: string
  extract_type?: string
}

export interface ValidatorData {
  comparator: string
  expect: any
  value: any
}

export interface ApiBodyFileDataSchema {
  key: string
  type: string
  desc?: string
}

export interface ApiBodyFileValueSchema {
  key: string
  value: string
  type: string
}

export interface TRequestData {
  comparator?: string
  image?: string
  dragImage?: string
  text?: string
  keys?: string[]
  picture_is_search?: boolean
  waitElementType?: string
  wait_time?: number
  [key: string]: any
}

export interface TApiData {
  url: string
  method: string
  headers?: Record<string, string>
  body?: any
  params?: Record<string, string>
}

export interface TSqlRequest {
  host: string
  port: number
  database: string
  username: string
  password: string
  sql: string
  variable_name?: string
}

export interface TStepLoopData {
  loop_type: string
  loop_count?: number
  loop_variable?: string
  loop_list?: any[]
}

export interface TStepIFData {
  condition: string
  comparator: string
  expect: any
}

export interface TStepWaitData {
  wait_time: number
}

export interface TStepScriptData {
  script: string
  script_type?: string
}

export interface TUiRequestData {
  action: string
  selector?: string
  selector_type?: string
  value?: string
  timeout?: number
}
