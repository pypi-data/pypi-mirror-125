"""
pyPreservica AdminAPI module definition

A client library for the Preservica Repository web Administration and Management API
https://us.preservica.com/api/admin/documentation.html

author:     James Carr
licence:    Apache License 2.0

"""
from typing import Generator, List
import xml.etree.ElementTree

from pyPreservica.common import *

logger = logging.getLogger(__name__)


class AdminAPI(AuthenticatedAPI):

    def __add_xml_document(self, document_type: str, post_parameters: dict, document: str):
        headers = {HEADER_TOKEN: self.token, 'Content-Type': 'application/xml;charset=UTF-8'}
        request = self.session.post(f"https://{self.server}/api/admin/{document_type}", headers=headers,
                                    params=post_parameters,
                                    data=document.encode("utf-8"))
        if request.status_code == requests.codes.created:
            return request.status_code
        elif request.status_code == requests.codes.unauthorized:
            self.token = self.__token__()
            return self.__add_xml_document(document_type, post_parameters, document)
        else:
            logger.error(request.content.decode('utf-8'))
            raise RuntimeError(request.status_code, "__add_xml_document failed")

    def add_xml_schema(self, name: str, description: str, originalName: str, document: str):
        """
        Add a new XSD document to Preservica

        """
        params = {"name": name, "description": description, "originalName": originalName}
        targetNamespace = ""
        xml_tree = xml.etree.ElementTree.fromstring(document)
        if 'targetNamespace' in xml_tree.attrib:
            targetNamespace = xml_tree.attrib['targetNamespace']

        self.__add_xml_document(document_type="schemas", post_parameters=params, document=document)
        return targetNamespace

    def add_xml_document(self, name: str, document: str, document_type: str = "MetadataTemplate"):
        """
        Add a new XML document to Preservica

        """
        params = {"name": name, "type": document_type}
        xml.etree.ElementTree.fromstring(document)
        self.__add_xml_document("documents", params, document)


    def delete_metadata_schema(self, uri: str):
        """
        Add a new XSD document to Preservica

        """
        headers = {HEADER_TOKEN: self.token, 'Content-Type': 'application/xml;charset=UTF-8'}

        for schema in self.metadata_schemas():
            if schema['SchemaUri'] == uri.strip():
                request = self.session.delete(f"https://{self.server}/api/admin/schemas/{schema['ApiId']}",
                                              headers=headers)
                if request.status_code == requests.codes.no_content:
                    return
                elif request.status_code == requests.codes.unauthorized:
                    self.token = self.__token__()
                    return self.metadata_schema(uri)
                else:
                    logger.error(request.content.decode('utf-8'))
                    raise RuntimeError(request.status_code, "metadata_schema failed")

    def metadata_schema(self, uri: str) -> str:
        """
         fetch the metadata schema XSD document as a string by its URI

         """
        headers = {HEADER_TOKEN: self.token, 'Content-Type': 'application/xml;charset=UTF-8'}

        for schema in self.metadata_schemas():
            if schema['SchemaUri'] == uri.strip():
                request = self.session.get(f"https://{self.server}/api/admin/schemas/{schema['ApiId']}/content",
                                           headers=headers)
                if request.status_code == requests.codes.ok:
                    xml_response = str(request.content.decode('utf-8'))
                    return xml_response
                elif request.status_code == requests.codes.unauthorized:
                    self.token = self.__token__()
                    return self.metadata_schema(uri)
                else:
                    logger.error(request.content.decode('utf-8'))
                    raise RuntimeError(request.status_code, "metadata_schema failed")

    def metadata_schemas(self) -> List:
        """
         fetch the list of metadata schema XSD documents stored in Preservica

         """
        headers = {HEADER_TOKEN: self.token, 'Content-Type': 'application/xml;charset=UTF-8'}

        request = self.session.get(f'https://{self.server}/api/admin/schemas', headers=headers)
        if request.status_code == requests.codes.ok:
            xml_response = str(request.content.decode('utf-8'))
            logger.debug(xml_response)
            entity_response = xml.etree.ElementTree.fromstring(xml_response)
            schemas = entity_response.findall(f'.//{{{self.admin_ns}}}Schema')
            results = list()
            for schema in schemas:
                schema_dict = {}
                schema_uri = schema.find(f'.//{{{self.admin_ns}}}SchemaUri')
                name = schema.find(f'.//{{{self.admin_ns}}}Name')
                description = schema.find(f'.//{{{self.admin_ns}}}Description')
                aip_id = schema.find(f'.//{{{self.admin_ns}}}ApiId')
                schema_dict['SchemaUri'] = schema_uri.text
                schema_dict['Name'] = name.text
                schema_dict['Description'] = description.text
                schema_dict['ApiId'] = aip_id.text
                results.append(schema_dict)
            return results

        elif request.status_code == requests.codes.unauthorized:
            self.token = self.__token__()
            return self.metadata_schemas()
        else:
            logger.error(request.content.decode('utf-8'))
            raise RuntimeError(request.status_code, "metadata_schemas failed")
