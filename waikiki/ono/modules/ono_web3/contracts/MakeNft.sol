// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;
 
import "./tokens/nf-token-metadata.sol";
import "./ownership/ownable.sol";
 
contract newNFT is NFTokenMetadata, Ownable {

  constructor(string memory _nftName, string memory _nftSymbol) {
    nftName = _nftName;
    nftSymbol = _nftSymbol;
  }
 
  function mint(address _to, uint256 _tokenId, string calldata _uri) external {
    super._mint(_to, _tokenId);
    super._setTokenUri(_tokenId, _uri);
  }
 
}