class GitReflux < Formula
  include Language::Python::Virtualenv
  desc "Human-friendly reflog CLI"
  homepage "https://github.com/alireza/git-reflux"
  url "https://files.pythonhosted.org/packages/source/g/git-reflux/git-reflux-0.1.0.tar.gz"
  sha256 "REPLACE_ME"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"git-reflux", "--version"
  end
end

