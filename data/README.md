``
<div align="center">
  
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=250&section=header&text=Spring%20Boot%20&%20System%20Design&fontSize=50&fontAlignY=50" alt="Banner" />

  <h1>🚀 Meu Framework de Desenvolvimento Backend</h1>
  <p><i>Um guia prático e opinativo de como eu desenvolvo APIs escaláveis, limpas e prontas para produção no Spring Boot.</i></p>

  <img src="https://img.shields.io/badge/Java-17+-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java" />
  <img src="https://img.shields.io/badge/Spring_Boot-3.x-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white" alt="Spring Boot" />
  <img src="https://img.shields.io/badge/Arquitetura-Layered-316192?style=for-the-badge" alt="Arquitetura" />
  <img src="https://img.shields.io/badge/Status-Em_Evolução-FFD700?style=for-the-badge" alt="Status" />

</div>

<br>

## 📌 Sobre o Projeto

Este repositório não é apenas código. É o meu **framework pessoal de desenvolvimento backend**, onde aplico:
- Boas práticas de programação.
- Arquitetura limpa.
- Princípios sólidos de engenharia de software.
- Padrões usados em sistemas reais.

O objetivo aqui é mostrar **como eu penso, estruturo e desenvolvo software backend**.

---

## 📑 Índice Interativo

- [1. Filosofia de Desenvolvimento 🧠](#-1-filosofia-de-desenvolvimento)
- [2. Estrutura do Projeto 📂](#-2-estrutura-do-projeto)
- [3. Setup Inicial 🛠️](#-3-setup-inicial-️)
- [4. A Mão na Massa (Fluxo Completo) 💻](#-4-a-mão-na-massa-fluxo-completo)
- [5. Tratamento de Erros e Boas Práticas 🛡️](#-5-tratamento-de-erros-e-boas-práticas-️)
- [6. Segurança (Spring Security & JWT) 🔒](#-6-segurança-spring-security--jwt)
- [7. Escalabilidade e System Design 🚀](#-7-escalabilidade-e-system-design)
- [8. Testes e Qualidade (Garantia de Entrega) 🧪](#-8-testes-e-qualidade-garantia-de-entrega)
- [9. Documentação Interativa (Swagger / OpenAPI) 📚](#-9-documentação-interativa-swagger--openapi)
- [10. Ambiente e Deploy (Docker) 🐳](#-10-ambiente-e-deploy-docker)
- [11. Observabilidade e Monitoramento 📊](#-11-observabilidade-e-monitoramento)

---

## 🧠 1. Filosofia de Desenvolvimento

Antes de escrever a primeira linha de código, eu sigo regras claras. O objetivo é criar uma forma que reflita o que deve ser feito. Tornando-o claro e eficiente.

### 📐 Princípios Base
* **SOLID:** Foco em classes com responsabilidades únicas e baixo acoplamento.
* **DRY (Don't Repeat Yourself):** Reutilização inteligente de código.
* **KISS (Keep It Simple, Stupid):** Soluções simples para problemas complexos.

### 🧹 Clean Code (Código Limpo)
* **Nomenclatura Clara:** Nada de `x`, `y` ou `aux`. Se busca um usuário por ID, o método se chama `findUserById()`.
* **Métodos Pequenos:** Um método deve fazer **apenas uma coisa**. Passou de 20 linhas? Extraia a lógica.
* **Inglês como Padrão:** Código e commits em inglês para facilitar a integração global.
* **Comentários são a exceção:** O código deve ser autoexplicativo. Comente o *porquê* de uma regra complexa, não o *que* o código faz.

> [!WARNING]  
> **Regras de Ouro:**
> 1. **Nunca vaze a Entidade:** Entidades (`@Entity`) não chegam ao Controller. Use **DTOs** para entrada e saída.
> 2. **Erros Centralizados:** Sem `try-catch` espalhados. Use `@ControllerAdvice`.

---

## 📂 2. Estrutura do Projeto

Separação rígida de responsabilidades: **Controller ➝ Service ➝ Repository**.

```text
src/main/java/com/meuframework/app
├── config/       # Configurações globais e Setup (Segurança, CORS).
├── controller/   # Entradas HTTP e devolução de Respostas HTTP.
├── dto/          # Data Transfer Objects (Request e Response).
├── model/        # Entidades de domínio (Tabelas do banco com JPA).
├── repository/   # Camada de acesso a dados (JpaRepository).
├── service/      # Regras de negócio e validações.
├── exception/    # Erros customizados e GlobalExceptionHandler.
└── infra/        # Integrações externas (RabbitMQ, Kafka, AWS).
````

-----

## 🛠️ 3. Setup Inicial

### 🔧 Dependências Base

  * **Spring Web:** Traz o Tomcat e anotações REST.
  * **Spring Data JPA:** Abstrai o SQL e JDBC.
  * **Lombok:** Remove a necessidade de digitar Getters e Setters.
  * **Validation:** Valida DTOs de entrada.
  * **PostgreSQL Driver & Flyway:** Banco de dados e controle de versão de schemas.

### 📄 `application.yml`

```yaml
server:
  port: 8080 

spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/meubanco
    username: root
    password: 123
  jpa:
    hibernate:
      ddl-auto: validate # Flyway/Liquibase assume o controle em prod
    show-sql: true
```

-----

## 💻 4. A Mão na Massa (Fluxo Completo)

### 🧩 Model (Entity) & 🔄 DTOs

```java
@Entity
@Table(name = "usuarios")
@Data
public class Usuario {
    @Id 
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String nome;
    private String email;
    private boolean ativo = true;
}

// O que o usuário envia
@Data
public class UsuarioCriarDTO {
    private String nome;
    private String email;
}

// O que nós devolvemos
@Data 
@AllArgsConstructor
public class UsuarioRespostaDTO {
    private Long id;
    private String nome;
    private String email;
}
```

### 🗄️ Repository & 🧠 Service

```java
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    boolean existsByEmail(String email);
}

@Service
public class UsuarioService {
    private final UsuarioRepository repository;

    // DIP: Injeção via construtor
    public UsuarioService(UsuarioRepository repository) {
        this.repository = repository;
    }

    public Usuario criar(UsuarioCriarDTO dto) {
        if (repository.existsByEmail(dto.getEmail())) {
            throw new RuntimeException("Email já existe");
        }
        
        Usuario user = new Usuario();
        user.setNome(dto.getNome());
        user.setEmail(dto.getEmail());
        
        return repository.save(user);
    }
}
```

### 🌐 Controller

```java
@RestController
@RequestMapping("/api/usuarios")
public class UsuarioController {
    private final UsuarioService service;

    public UsuarioController(UsuarioService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<UsuarioRespostaDTO> criar(@RequestBody UsuarioCriarDTO dto) {
        Usuario user = service.criar(dto);
        return ResponseEntity.ok(
            new UsuarioRespostaDTO(user.getId(), user.getNome(), user.getEmail())
        );
    }
}
```

-----

## 🛡️ 5. Tratamento de Erros e Boas Práticas

### 🚦 Padrões RESTful Inegociáveis

  * **URLs:** Sempre no plural e sem verbos (`GET /api/usuarios`).
  * **Aninhamento Curto:** Máximo de 2 níveis (`/api/pedidos/7/itens`).
  * **Status HTTP:** `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `404 Not Found`.

### 🚨 Exception Handler Global

```java
public record ErrorResponse(String timestamp, int status, String erro, Object detalhes, String path) {}

@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> handle(Exception ex) {
        return ResponseEntity.badRequest().body(ex.getMessage());
    }
}
```

-----

## 🔒 6. Segurança (Spring Security & JWT)

A API adota o padrão **Stateless** com **JWT (JSON Web Tokens)**.

> [\!TIP]
> **Checklist de Segurança:**
>
>   * [x] Senhas criptografadas (BCrypt).
>   * [x] JWT Stateless (Enviado via header `Authorization: Bearer <token>`).
>   * [x] Variáveis de ambiente para segredos.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated()
            );
        return http.build();
    }
}
```

-----

## 🚀 7. Escalabilidade e System Design

Quando escalar de **Monolito** para **Microsserviços**, as estratégias são:

  * **Comunicação Síncrona:** HTTP via **OpenFeign** com **Circuit Breaker** (Resilience4j) para evitar falhas em cascata.
  * **Comunicação Assíncrona:** Mensageria via **RabbitMQ** ou **Kafka** para desacoplar tarefas pesadas (ex: envio de e-mails, processamento de relatórios).
  * **Dados:** Implementação de **Redis** (`@Cacheable`) para alívio de banco de dados e estratégias de *Read Replicas* no PostgreSQL.

-----

## 🧪 8. Testes e Qualidade (Garantia de Entrega)

O Código não pode ir para produção sem garantia de que funciona. O desenvolvimento é guiado por testes para evitar regressões e garantir a integridade das regras de negócio.

  * **JUnit 5 & Mockito:** Para testes unitários isolados da camada de `Service`.
  * **Testcontainers:** Para testes de integração reais subindo um banco PostgreSQL efêmero via Docker.

<!-- end list -->

```java
@ExtendWith(MockitoExtension.class)
class UsuarioServiceTest {

    @Mock
    private UsuarioRepository repository;

    @InjectMocks
    private UsuarioService service;

    @Test
    @DisplayName("Deve lançar exceção ao tentar criar usuário com email já existente")
    void deveLancarExcecaoQuandoEmailJaExiste() {
        // Arrange
        UsuarioCriarDTO dto = new UsuarioCriarDTO("João", "joao@email.com");
        when(repository.existsByEmail(dto.getEmail())).thenReturn(true);

        // Act & Assert
        assertThrows(RuntimeException.class, () -> service.criar(dto));
        verify(repository, never()).save(any(Usuario.class));
    }
}
```

-----

## 📚 9. Documentação Interativa (Swagger / OpenAPI)

Uma API só é útil se quem for consumir souber como usá-la. Ninguém precisa ler o código-fonte para entender os endpoints.

Utilizamos o **SpringDoc OpenAPI** para gerar a documentação viva da API.

  * **Acesso local:** `http://localhost:8080/swagger-ui.html`
  * Os endpoints são descritos com exemplos de Request, Response e mapeamento de todos os Status HTTP possíveis.

-----

## 🐳 10. Ambiente e Deploy (Docker)

O projeto é construído para rodar em qualquer lugar, sem a desculpa do *"na minha máquina funciona"*.

Com apenas um comando, toda a infraestrutura (Banco de Dados, Filas, Cache e a própria Aplicação) sobe padronizada usando o `docker-compose`.

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 123
      POSTGRES_DB: meubanco
    ports:
      - "5432:5432"

  api:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/meubanco
```

**Para rodar:** `docker-compose up -d`

-----

## 📊 11. Observabilidade e Monitoramento

Sistemas falham, e quando isso acontece, precisamos de rastreabilidade.

  * **Logs Estruturados (SLF4J/Logback):** Padronização de logs de erro e info.
  * **Spring Boot Actuator:** Exposição do endpoint `/actuator/health` para que ferramentas de infraestrutura (como Kubernetes) saibam se a aplicação está saudável e pronta para receber tráfego.

<br>

> ⚡ *"O desenvolvimento de software é uma jornada repleta de desafios e conquistas. Manter a motivação alta faz toda a diferença para um programador alcançar o sucesso."*

<div align="center">
  <b>Desenvolvido com foco em Software Engineer por <a href="[https://github.com/Alef71](https://github.com/Alef71)">Álef Francisco Ribeiro Amaral</a></b>
</div>
