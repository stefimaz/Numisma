{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "pragma solidity ^0.5.0;\n",
    "\n",
    "import \"https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol\";\n",
    "import \"https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol\";\n",
    "import \"https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol\";\n",
    "\n",
    "contract MetaDex is ERC20, ERC20Detailed {\n",
    "    address payable owner;\n",
    "\n",
    "    modifier onlyOwner {\n",
    "        require(msg.sender == owner, \"You do not have the permission to mint these tokens!\");\n",
    "        _;\n",
    "    }\n",
    "    constructor(uint initial_supply) ERC20Detailed(\"MetaDex\", \"MDX\", 18) public {\n",
    "        owner = msg.sender;\n",
    "        _mint(owner, initial_supply);\n",
    "    }\n",
    "    \n",
    "    function mint(address recipient, uint amount) public onlyOwner {\n",
    "        _mint(recipient, amount);\n",
    "    }   \n",
    "\n",
    "} "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
