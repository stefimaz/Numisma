pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract MetaNFT is ERC721Full {
    constructor() public ERC721Full("metaNFT", "MNF") {}

    function metaNFT(address investor, uint256 amount, string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newInvestorId = totalSupply();
        _mint(investor, newInvestorId);
        _setTokenURI(newInvestorId, tokenURI);

        return newInvestorId;
    }
}