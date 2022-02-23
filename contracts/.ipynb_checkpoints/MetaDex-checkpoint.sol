pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract MetaDex is ERC721Full {
    constructor() public ERC721Full("metaDex", "MDX") {}

    struct Investment {
        string name;
        string theme;
        uint256 initialInvestment;
    }

    mapping(uint256 => Investment) public investmentPortfolio;

    event Porfolio(uint256 token_id, uint256 initialInvesment, string reportURI);

    function registerInvestment(
        address owner,
        string memory name,
        string memory theme,
        uint256 initialInvestment,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        investmentPortfolio[tokenId] = Investment(name, theme, initialInvestment);

        return tokenId;
    }

    function newAppraisal(
        uint256 tokenId,
        uint256 newValue,
        string memory reportURI
    ) public returns (uint256) {
        investmentPortfolio[tokenId].Value = newValue;

        emit Portfolio(tokenId, newInvestment, reportURI);

        return investmentPortfolio[tokenId].Value;
    }
}