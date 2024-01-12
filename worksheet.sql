--------------------------------------------------------------------------
-- Set context
--------------------------------------------------------------------------
use role accountadmin;
create warehouse if not exists compute_wh;
use warehouse compute_wh;
create database if not exists external_functions;
create schema if not exists external_functions.vrs;
use schema external_functions.vrs;

--------------------------------------------------------------------------
-- Create Azure API integration
--------------------------------------------------------------------------
create or replace api integration azure_function_integration
    api_provider = azure_api_management
    azure_tenant_id = '9a2d78cb-73e9-40ee-a558-fc1ac5ef57a7'
    azure_ad_application_id = '1be057aa-97ef-4eb8-9516-ad03571f058f'
    api_allowed_prefixes = ('https://kgaputis-api-management-service.azure-api.net')
    enabled = true;
describe api integration azure_function_integration;

--------------------------------------------------------------------------
-- Link the API Integration for Azure to the Proxy Service in the Portal
--------------------------------------------------------------------------
-- See: https://docs.snowflake.com/en/sql-reference/external-functions-creating-azure-common-api-integration-proxy-link

--------------------------------------------------------------------------
-- Create external function for parsing GA4GH identifiers using VRS
-- (this has no data service dependency)
--------------------------------------------------------------------------
create or replace external function parse_ga4gh_identifier(identifier varchar)
    returns variant
    returns null on null input
    immutable
    api_integration = azure_function_integration
    as 'https://kgaputis-api-management-service.azure-api.net/kgaputis-vrs-function-app/parse-ga4gh-identifier';
describe function parse_ga4gh_identifier(varchar);

SELECT parse_ga4gh_identifier('ga4gh:VCL.eLG0pS7t_p8cqfm_SG4xLFDCPbkyGt0t');

--------------------------------------------------------------------------
-- Create external function for translating various expressions into GA4GH allele IDs
--------------------------------------------------------------------------
create or replace external function identify_allele(expr varchar, format varchar)
    returns variant
    returns null on null input
    immutable
    api_integration = azure_function_integration
    as 'https://kgaputis-api-management-service.azure-api.net/kgaputis-vrs-function-app/identify-allele';
describe function identify_allele(varchar, varchar);

SELECT identify_allele('NC_000019.10:g.44908822=','hgvs');
SELECT identify_allele('NC_000009.12:128325834:C:T','spdi');

SELECT parse_ga4gh_identifier('ga4gh:VA.IIHnU7xKQBzTkz_hR_A6dMxnLuCwFKzc');


