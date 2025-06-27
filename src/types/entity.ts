
export interface Entity {
  id: number;
  //#TODO id should be uuid?? new ObjectId()
  name: string;
  entity_type: string;
  entity_parent?: Entity;
}
