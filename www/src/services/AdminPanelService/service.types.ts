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

export interface INewsEntityData {
  id: number;
  url: string;
  name: string;
  description: string;
  vendor: string;
  field_tags: string;
  is_enable: string;
  parser_id: number;
}

export interface ICatalogEntityData {
  id: number;
  name: string;
  url: string;
  description: string;
  is_enable: string;
  parser_id: number;
}

export interface IInternetSiteDTO {
  id: number;
  name: string;
  description: string;
  news_gathering_id: number;
  catalog_gathering_id: number;
}
