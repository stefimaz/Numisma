// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Vdex is ERC20 {

    address payable owner;
    address payable wallet;
    uint public exchange_rate = 100;
    

    mapping(address => uint) balances;

    modifier OnlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }
    constructor() ERC20("vdex", "VDX") {
        _mint(msg.sender, 10000 * 10 ** decimals());
    }

    function mint(address recipient, uint amount) public OnlyOwner {
        _mint(recipient, amount);
    }

    function purchase(address payable, uint256) public payable {      
        uint amount = msg.value * (exchange_rate);
        balances[msg.sender] = balances[msg.sender] + (amount);
        owner.transfer(msg.value);
    }

 //   function withdraw() public onlyOwner {
 //       require(address(this).balance > 0, "Balance is 0!");
 //       payable(owner()).transfer(address(this).balance);
 //   }
}
