# File Converter

- CSV para conversor JSON.
- JSON para conversor CSV.

## Introdução

### O que este projeto pode fazer

- Leia um arquivo **csv** ou uma **pasta** com csv's e converta-os em **JSON**.
- Leia um arquivo **json** ou uma **pasta** com json's e converta-os em **CSV**.

Este projeto é um programa em execução no terminal, de preferência instalado com pipx:

`` `bash
pipx install clebs-puc-csv-converter
`` `

Para usar, basta digitar:

`` `bash
$ converter --help
`` `

Isso listará todas as opções disponíveis.

`` `
Usage: converter [OPTIONS] {csv|json}

  Convert Single file or list of CSV files to json or json to convert json
  files to csv.

Options:
  -i, --input TEXT            Path where the files will be loaded for conversion.
  -o, --output TEXT           Path where the converted files will be saved.
  -d, --delimiter [,|;|:|\t]  Separator used to split the files.
  -p, --prefix TEXT           Prefix used to prepend to the name of the converted
                            file saved on disk. The suffix will be a number
                            starting from 0. ge: file_0.json.
  --help                      Show this message and exit.
`` `
