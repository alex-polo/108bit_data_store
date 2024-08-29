export interface IParserData {
  id: number;
  system_name: string;
  parser_name: string;
  description: string;
  parser_type: string;
  is_enable: string;
  is_parser_scheme_missing: string;
}

export interface IParserChangeData {
  system_name: string;
  parser_name: string;
  description: string;
  is_enable: string;
}
