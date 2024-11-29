# Documentação de Funcionalidade para o Módulo de API de Autenticação (Flask)

## Introdução

Este documento descreve a proposta para o desenvolvimento de um módulo de API de autenticação em Flask. O objetivo do módulo é fornecer autenticação baseada em JWT (JSON Web Tokens) para um sistema web, garantindo segurança e flexibilidade no controle de acesso.

### Objetivos
1. Permitir o registro de usuários.
2. Autenticar usuários e fornecer tokens de acesso e atualização.
3. Identificar o usuário autenticado.
4. Renovar tokens de acesso expirados.
5. Realizar logout, invalidando tokens emitidos anteriormente.

## Funcionalidades Propostas

### **1. Registro de Usuários (`/register`)**
- **Descrição**: Endpoint para cadastrar novos usuários no sistema.
- **Requisitos**:
  - Receber `username`, `email` e `password` no corpo da requisição.
  - Verificar se o nome de usuário já existe.
  - Armazenar o usuário no banco de dados com senha criptografada.
- **Melhorias**:
  - **Validação Avançada**: Implementar validação mais robusta, como verificação de força de senha e formato de e-mail.
  - **Verificação de E-mail**: Adicionar lógica para envio de e-mail de confirmação para ativar a conta do usuário.

---

### **2. Login de Usuários (`/login`)**
- **Descrição**: Endpoint para autenticar um usuário e emitir tokens JWT.
- **Requisitos**:
  - Validar credenciais (nome de usuário e senha).
  - Emitir tokens JWT (acesso e atualização) para usuários autenticados.
- **Melhorias**:
  - **Proteção contra Força Bruta**: Adicionar limite de tentativas de login para evitar ataques de força bruta.
  - **Registro de Logs**: Implementar registro de logs para auditoria de acessos (IP, horário, tentativas).

---

### **3. Identificação do Usuário Autenticado (`/userinfo`)**
- **Descrição**: Endpoint que retorna informações sobre o usuário autenticado.
- **Requisitos**:
  - Utilizar JWT para autenticar a requisição.
  - Retornar detalhes do usuário (nome de usuário e e-mail).
- **Melhorias**:
  - **Permissões Baseadas em Funções**: Incluir lógica para verificar e retornar os papéis (roles) do usuário.
  - **Auditoria**: Registrar no log o acesso a este endpoint.

---

### **4. Renovação de Tokens (`/refresh`)**
- **Descrição**: Endpoint para renovar tokens de acesso expirados usando o token de atualização.
- **Requisitos**:
  - Requer autenticação com um token de atualização válido.
  - Emitir um novo token de acesso.
- **Melhorias**:
  - **Rotação de Tokens**: Implementar rotação de tokens de atualização, onde um token de atualização é emitido junto com o novo token de acesso.
  - **Blacklisting**: Revogar tokens de atualização após o uso para prevenir reutilização.

---

### **5. Logout de Usuários (`/logout`)**
- **Descrição**: Endpoint para invalidar tokens (tanto de acesso quanto de atualização).
- **Requisitos**:
  - Requer autenticação JWT.
  - Adicionar o JTI (JWT ID) na lista de bloqueio.
- **Melhorias**:
  - **Logout Global**: Implementar lógica para invalidar todos os tokens ativos do usuário.
  - **Feedback Detalhado**: Informar ao usuário quais tipos de tokens foram revogados (acesso, atualização ou ambos).

---

## Melhorias Globais

### **1. Controle de Acesso Baseado em Funções**
- Implementar um sistema de permissões onde endpoints específicos só podem ser acessados por usuários com papéis específicos, como "admin" ou "usuário padrão".

### **2. Auditoria e Logging**
- Configurar o registro de logs detalhados para todas as ações:
  - Tentativas de login.
  - Acessos bem-sucedidos e falhos.
  - Operações sensíveis (logout, renovação de tokens).
- Garantir que logs sensíveis não contenham informações como senhas ou tokens.

### **3. Segurança**
- **CSRF (Cross-Site Request Forgery)**: Adicionar proteção contra CSRF em endpoints críticos.
- **HSTS (HTTP Strict Transport Security)**: Forçar o uso de HTTPS para todas as requisições.
- **Blacklist Persistente**: Garantir que tokens bloqueados sejam armazenados e checados de forma eficiente.

### **4. Testes**
- Desenvolver uma suíte de testes automatizados para cobrir todos os endpoints e cenários, incluindo:
  - Testes de carga.
  - Testes de vulnerabilidades (como ataques de repetição de token).

---

## Estrutura Esperada da API

| Método | Endpoint        | Descrição                  | Autenticação |
|--------|-----------------|----------------------------|--------------|
| POST   | `/register`     | Registrar um novo usuário. | Não          |
| POST   | `/login`        | Autenticar o usuário.      | Não          |
| GET    | `/userinfo`       | Identificar o usuário.     | JWT          |
| GET    | `/refresh`      | Renovar token de acesso.   | JWT (refresh)|
| GET    | `/logout`       | Logout do usuário.         | JWT          |


  