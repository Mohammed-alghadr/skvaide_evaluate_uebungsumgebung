{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
	devcontainer.enable = true;
	
	languages.python = {
	enable = true;
	package = pkgs.python313;
	uv = {
		enable = true;
		sync.enable = true;
		};
	};
  
}
