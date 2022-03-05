// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract VentidexToken is ERC721, ERC721Enumerable, ERC721URIStorage, ERC721Burnable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    using Strings for uint256;

    uint256 public mintRate = 0.3 ether;
    uint public Max_supply = 200000;

    string baseURI;
    string public baseExtension = ".json";

    address public artist;
    uint256 public royalityFee;

    event Sale(address from, address to, uint256 value);  

    constructor() ERC721("VentidexToken", "VTX") {
            
        }

    struct Portfolio {
        string name ;
        string portfolio;
        uint256 distributionValue;
    }
    struct Index{
        string name;
        string holder;
        uint initialIndexValue;
    }

    mapping(address => uint) balances;

    mapping(uint256 => Index) public portfolio;

    event Appraisal(uint256 tokenId, uint256 indexValue);

    function _baseURI() internal pure override returns (string memory) {
        return "https://gateway.pinata.cloud/ipfs/QmTRwDATJ7GuRtKJQWUjigYLoepokwCAKxjxS4Ti19NbDn";
    }

    function mint() public payable {
        uint256 supply = totalSupply();          
        require(totalSupply() <= Max_supply, "This portfolio is Soldout!");
        require(supply < Max_supply, "Exceeds maximum supply");
     //   require(msg.value >= mintRate, "Not enought Ether sent");
        
       // uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        

     //   uint256 royality = (msg.value * royalityFee) / 100;
      //  _payRoyality(royality);

      //  (bool success2, ) = payable(owner()).call{
     //           value: (msg.value - royality)
    //        }("");
     //       require(success2);
      //  for(uint256 i; i < num; i++){}//
      //  _safeMint(msg.sender, supply + i);
    }
    
    function registerPortfolio(
        address owner,
        string memory name,
        string memory holder,
        uint256 initialIndexValue
        
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        

        portfolio[tokenId] = Index(name, holder, initialIndexValue);

        return tokenId;
    }
    // The following functions are overrides required by Solidity.

    function _beforeTokenTransfer(address from, address to, uint256 tokenId)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
     function withdraw() public onlyOwner {
        require(address(this).balance > 0, "Balance is 0!");
        payable(owner()).transfer(address(this).balance);
    }  

    function _payRoyality(uint256 _royalityFee) internal {
        (bool success1, ) = payable(artist).call{value: _royalityFee}("");
        require(success1);
    }

    // Owner functions
    function setRoyalityFee(uint256 _royalityFee) public onlyOwner {
        royalityFee = _royalityFee;
    }
}