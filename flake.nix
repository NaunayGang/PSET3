{
  description = "PSET3: OpsCenter Internal Management Platform";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    resources.url = "git+https://codeberg.org/yuuhikaze/resources";
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      resources,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = pkgs.python3.withPackages (
          ps: with ps; [
            fastapi
            streamlit
            uvicorn
            sqlalchemy
            psycopg2
            pydantic
            pydantic-settings
            email-validator
            pytest
            httpx
            requests
            python-multipart
            python-jose
            passlib
            bcrypt
          ]
        );
      in
      {
        devShells.default = pkgs.mkShell {
          inputsFrom = [ resources.outputs.devShells.${system}.docs ];
          buildInputs = [
            pythonEnv
            pkgs.docker
            pkgs.docker-compose
            pkgs.git
          ];
          shellHook = ''
             echo "====== OpsCenter PSET3 Development Environment ======="
            echo "Python: $(python --version)"
            echo "Docker: $(docker --version)"
            echo "============================================"
          '';
        };
      }
    );
}
